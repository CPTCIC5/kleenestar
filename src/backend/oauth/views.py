from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel
import hashlib
import urllib.parse 
import os
import base64
from google_auth_oauthlib.flow import Flow
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session, OAuth1
from django.shortcuts import redirect
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
from twitter_ads.client import Client
from twitter_ads.campaign import Campaign, LineItem
from twitter_ads.analytics import Analytics
from twitter_ads.creative import PromotedTweet
from users.models import User
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
import random
import string
# PromotedTweet = PromotedTweet.attach()
load_dotenv()


def get_channel(email,channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]
    return get_object_or_404(Channel, channel_type=channel_type_num, workspace=workspace)


#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

#google
credentials = {
"developer_token": os.getenv("GOOGLE_DEVELOPER_TOKEN"),
"client_id": os.getenv("GOOGLE_CLIENT_ID"),
"client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
"use_proto_plus": "false"
}
google_redirect_uri = 'http://127.0.0.1:8000/api/oauth/google-callback/'
google_scopes = ["openid","https://www.googleapis.com/auth/adwords" ,"https://www.googleapis.com/auth/userinfo.email" ,"https://www.googleapis.com/auth/userinfo.profile"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Adjusted to navigate to the project root
google_client_secret_file = os.path.join(BASE_DIR, 'oauth', 'utils', 'XYZ.json')
flow = Flow.from_client_secrets_file(google_client_secret_file, scopes=google_scopes)
flow.redirect_uri = google_redirect_uri


#facebook
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
facebook_authorization_base_url = 'https://www.facebook.com/dialog/oauth'
facebook_redirect_uri = 'https://127.0.0.1:8000/api/oauth/facebook-callback/'
facebook_scopes = ['ads_read','ads_management','public_profile','email']  
facebook = OAuth2Session(facebook_client_id, redirect_uri=facebook_redirect_uri, scope=facebook_scopes)
facebook = facebook_compliance_fix(facebook)
facebook_token_url = 'https://graph.facebook.com/oauth/access_token'


#twitter
twitter_client_id = os.getenv("TWITTER_CLIENT_ID")
twitter_client_secret = os.getenv("TWITTER_CLIENT_SECRET")
twitter_redirect_uri = 'http://127.0.0.1:8000/api/oauth/twitter-callback/'
twitter_authorization_base_url = "https://api.twitter.com/oauth/authenticate"
twitter_token_url = "https://api.twitter.com/oauth/access_token"
twitter_scopes = ["email", "ads_read", "ads_management"]
twitter_ads_api_url = 'https://ads-api.twitter.com/'
twitter_api_version = '11'
resource_owner_key = ''
resource_owner_secret = ''

#linkedin
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_scope = ["r_ads_reporting", "r_ads", "r_organization_admin", "email","openid","profile","r_organization_social"]
linkedin_authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
linkedin_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
linkedin_redirect_uri = 'http://127.0.0.1:8000/api/oauth/linkedin-callback/'
linkedin = OAuth2Session(linkedin_client_id, redirect_uri=linkedin_redirect_uri, scope=linkedin_scope)

#tiktok
tiktok_client_id = os.getenv('TIKTOK_CLIENT_ID')
tiktok_client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
tiktok_redirect_uri = 'https://127.0.0.1:8000/api/oauth/tiktok-callback/'
tiktok_authorization_base_url = 'https://www.tiktok.com/v2/auth/authorize/'
tiktok_token_url = 'https://www.tiktok.com/v2/auth/authorize/'
tiktok_scopes = ['ads.read', 'ads.management', 'user.info']
tiktok = OAuth2Session(client_id=tiktok_client_id, redirect_uri=tiktok_redirect_uri, scope=tiktok_scopes)

#-----------------------------------------------------GOOGLE--------------------------------------------------#

@api_view(("GET",))
def google_oauth(request):
    try:
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            state=passthrough_val,
            prompt="consent",
            include_granted_scopes="true",
        )
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
def google_oauth_callback(request):

    # code to get access token from refresh token

    # refresh_token = 'your_refresh_token'
    # client_id = 'your_client_id'
    # client_secret = 'your_client_secret'
    # token_uri = 'https://oauth2.googleapis.com/token'


    # creds = Credentials.from_authorized_user_info({
    #     'refresh_token': refresh_token,
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    #     'token_uri': token_uri
    # })

    # if creds and creds.expired and creds.refresh_token:
    #     creds.refresh(Request())

    # access_token = creds.token

    # https://example.com/?code=...
    code = request.query_params.get("code")
    if not code:
        return Response(
        {"detail": "something not working???"},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    elif request.query_params.get("state") != passthrough_val:
        return Response(
        {"detail": "State token does not match the expected state."},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        flow.fetch_token(code=code)
        access_token = flow.credentials.token
        refresh_token = flow.credentials.refresh_token
        credentials["refresh_token"] = refresh_token

        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if response.status_code == 200:
            email = response.json().get('email')
        else:
            print(f"Failed to get user info: {response.content}")
            return Response(
                {"detail": "Failed to get user info"},
                status=status.HTTP_400_BAD_REQUEST
            )

        google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
        customer_service = google_client.get_service("CustomerService")

        accessible_customers = customer_service.list_accessible_customers()
        
        if len(accessible_customers.resource_names) > 1:
            return Response(
                {"detail": "Manager accounts not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        resource_names = accessible_customers.resource_names
        manager_id = resource_names[0].split('/')[1]
        
        #retrive all the client account ids of the manager account
        client_id_list = []
        query = """
            SELECT
                customer_client.client_customer,
                customer_client.level,
                customer_client.manager,
                customer_client.descriptive_name,
                customer_client.currency_code,
                customer_client.time_zone,
                customer_client.id
            FROM
                customer_client
            WHERE   
                customer_client.level <= 1
        """
        google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
        google_ads_service = google_client.get_service("GoogleAdsService")
        response = google_ads_service.search(customer_id=manager_id, query=query)
        for row in response:
            if(row.customer_client.id != int(manager_id)):
                client_id_list.append(str(row.customer_client.id))
        
        if len(client_id_list) == 0:
            return Response(
                {"detail": "No ads account found allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        
        google_channel = get_channel(
            email=email,
            channel_type_num=1
        )
        
        google_channel.credentials.key_1 = refresh_token
        google_channel.credentials.key_2 = access_token
        google_channel.credentials.key_3 = manager_id
        google_channel.credentials.key_4 = client_id_list
        google_channel.credentials.save()
        
        
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
def get_google_marketing_data(manager_id, client_id_list, refresh_token):

    credentials["refresh_token"] = refresh_token
    
    credentials["login_customer_id"] = manager_id

    google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
    marketing_data = []
    for id in client_id_list:
        
        # end_date = datetime.now().date()
        # start_date = end_date - timedelta(days=30)
        ga_service = google_client.get_service("GoogleAdsService")
        results = {
            "channel": "Goolge Ads",
            "campaigns": [],
            "ad_groups": [],
            "ad_group_ads": []
        }
        campaign_query = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.serving_status, campaign.advertising_channel_type, campaign.start_date, campaign.end_date, campaign.campaign_budget, campaign.target_cpa.cpc_bid_ceiling_micros, campaign.target_cpa.cpc_bid_floor_micros, campaign.target_cpa.target_cpa_micros, campaign_budget.id, campaign_budget.name, campaign_budget.period, campaign_budget.amount_micros, campaign_budget.status, campaign_budget.recommended_budget_estimated_change_weekly_views, campaign_budget.recommended_budget_estimated_change_weekly_interactions, campaign_budget.recommended_budget_estimated_change_weekly_cost_micros, campaign_budget.recommended_budget_estimated_change_weekly_clicks, campaign_budget.recommended_budget_amount_micros, campaign_budget.type, campaign_budget.total_amount_micros, campaign_group.id, campaign_group.name, campaign_group.resource_name, campaign_group.status, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM campaign"""  # + f"""WHERE segments.date BETWEEN {start_date} AND {end_date} """
        
        ad_group_query = """
        SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status, ad_group.campaign, ad_group.effective_target_cpa_micros, ad_group.effective_target_cpa_source, ad_group.type, ad_group.target_cpm_micros, ad_group.target_cpa_micros, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM ad_group """ # + f"""WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'""" 

        ad_group_ad_query = """ 
        SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.ad.text_ad.description1, ad_group_ad.ad.text_ad.description2, ad_group_ad.ad.type, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM ad_group_ad """  # + f"""WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'""" 
        keyword_view_query = """
        SELECT campaign.name, ad_group.name,keyword_view.resource_name, metrics.cost_micros, metrics.conversions_value, metrics.clicks, metrics.interaction_rate, metrics.view_through_conversions, metrics.average_cpc, metrics.conversions, metrics.ctr, metrics.all_conversions, metrics.cost_per_conversion, metrics.value_per_conversion, metrics.all_conversions_value, metrics.conversions_from_interactions_rate FROM keyword_view """
        try:
            campaign_response = ga_service.search(customer_id=id, query=campaign_query)
            campaign_data = []
            ad_group_response = ga_service.search(customer_id=id, query=ad_group_query)
            ad_group_data = []
            ad_group_ad_response = ga_service.search(customer_id=id, query=ad_group_ad_query)
            ad_group_ad_data = []
            keyword_view_response = ga_service.search(customer_id=id, query=keyword_view_query)
            keyword_view_data = []

            for campaign_row in campaign_response:
                campaign_data.append({
                    "campaign_id": campaign_row.campaign.id,
                    "campaign_name": campaign_row.campaign.name,
                    "campaign_status": campaign_row.campaign.status,
                    "campaign_serving_status": campaign_row.campaign.serving_status,
                    "campaign_advertising_channel_type": campaign_row.campaign.advertising_channel_type,
                    "campaign_start_date": campaign_row.campaign.start_date,
                    "campaign_end_date": campaign_row.campaign.end_date,
                    "campaign_budget": campaign_row.campaign.campaign_budget,
                    "campaign_target_cpa": {
                        "cpc_bid_ceiling_micros": campaign_row.campaign.target_cpa.cpc_bid_ceiling_micros,
                        "cpc_bid_floor_micros": campaign_row.campaign.target_cpa.cpc_bid_floor_micros,
                        "target_cpa_micros": campaign_row.campaign.target_cpa.target_cpa_micros
                    },
                    "campaign_budget_details": {
                        "budget_id": campaign_row.campaign_budget.id,
                        "budget_name": campaign_row.campaign_budget.name,
                        "period": campaign_row.campaign_budget.period,
                        "amount_micros": campaign_row.campaign_budget.amount_micros,
                        "status": campaign_row.campaign_budget.status,
                        "recommended_budget_estimated_change_weekly_views": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_views,
                        "recommended_budget_estimated_change_weekly_interactions": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_interactions,
                        "recommended_budget_estimated_change_weekly_cost_micros": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_cost_micros,
                        "recommended_budget_estimated_change_weekly_clicks": campaign_row.campaign_budget.recommended_budget_estimated_change_weekly_clicks,
                        "recommended_budget_amount_micros": campaign_row.campaign_budget.recommended_budget_amount_micros,
                        "type": campaign_row.campaign_budget.type_,
                        "total_amount_micros": campaign_row.campaign_budget.total_amount_micros,
                    },
                    "campaign_group": {
                        "group_id": campaign_row.campaign_group.id,
                        "group_name": campaign_row.campaign_group.name,
                        "resource_name": campaign_row.campaign_group.resource_name,
                        "status": campaign_row.campaign_group.status,
                    },
                    "metrics": {
                        "cost_micros": campaign_row.metrics.cost_micros,
                        "conversions_value": campaign_row.metrics.conversions_value,
                        "clicks": campaign_row.metrics.clicks,
                        "interaction_rate": campaign_row.metrics.interaction_rate,
                        "view_through_conversions": campaign_row.metrics.view_through_conversions,
                        "average_cpc": campaign_row.metrics.average_cpc,
                        "conversions": campaign_row.metrics.conversions,
                        "ctr": campaign_row.metrics.ctr,
                        "all_conversions": campaign_row.metrics.all_conversions,
                        "cost_per_conversion": campaign_row.metrics.cost_per_conversion,
                        "value_per_conversion": campaign_row.metrics.value_per_conversion,
                        "all_conversions_value": campaign_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": campaign_row.metrics.conversions_from_interactions_rate,
                    }
                })

            for ad_group_row in ad_group_response:
                ad_group_data.append({
                    "ad_group_id": ad_group_row.ad_group.id,
                    "ad_group_name": ad_group_row.ad_group.name,
                    "campaign_name": ad_group_row.campaign.name,
                    "ad_group_status": ad_group_row.ad_group.status,
                    "campaign_id": ad_group_row.ad_group.campaign,
                    "effective_target_cpa_micros": ad_group_row.ad_group.effective_target_cpa_micros,
                    "effective_target_cpa_source": ad_group_row.ad_group.effective_target_cpa_source,
                    "ad_group_type": ad_group_row.ad_group.type_,
                    "target_cpm_micros": ad_group_row.ad_group.target_cpm_micros,
                    "target_cpa_micros": ad_group_row.ad_group.target_cpa_micros,
                    "metrics": {
                        "cost_micros": ad_group_row.metrics.cost_micros,
                        "conversions_value": ad_group_row.metrics.conversions_value,
                        "clicks": ad_group_row.metrics.clicks,
                        "interaction_rate": ad_group_row.metrics.interaction_rate,
                        "view_through_conversions": ad_group_row.metrics.view_through_conversions,
                        "average_cpc": ad_group_row.metrics.average_cpc,
                        "conversions": ad_group_row.metrics.conversions,
                        "ctr": ad_group_row.metrics.ctr,
                        "all_conversions": ad_group_row.metrics.all_conversions,
                        "cost_per_conversion": ad_group_row.metrics.cost_per_conversion,
                        "value_per_conversion": ad_group_row.metrics.value_per_conversion,
                        "all_conversions_value": ad_group_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": ad_group_row.metrics.conversions_from_interactions_rate
                    }
                })

            for ad_group_ad_row in ad_group_ad_response:
                ad_group_ad_data.append({
                    "ad_id": ad_group_ad_row.ad_group_ad.ad.id,
                    "ad_name": ad_group_ad_row.ad_group_ad.ad.name,
                    "campaign_name": ad_group_ad_row.campaign.name,
                    "ad_group_name": ad_group_ad_row.ad_group.name,
                    "ad_status": ad_group_ad_row.ad_group_ad.status,
                    "final_urls": ad_group_ad_row.ad_group_ad.ad.final_urls,
                    "description1": ad_group_ad_row.ad_group_ad.ad.text_ad.description1,
                    "description2": ad_group_ad_row.ad_group_ad.ad.text_ad.description2,
                    "ad_type": ad_group_ad_row.ad_group_ad.ad.type_,
                    "metrics": {
                        "cost_micros": ad_group_ad_row.metrics.cost_micros,
                        "conversions_value": ad_group_ad_row.metrics.conversions_value,
                        "clicks": ad_group_ad_row.metrics.clicks,
                        "interaction_rate": ad_group_ad_row.metrics.interaction_rate,
                        "view_through_conversions": ad_group_ad_row.metrics.view_through_conversions,
                        "average_cpc": ad_group_ad_row.metrics.average_cpc,
                        "conversions": ad_group_ad_row.metrics.conversions,
                        "ctr": ad_group_ad_row.metrics.ctr,
                        "all_conversions": ad_group_ad_row.metrics.all_conversions,
                        "cost_per_conversion": ad_group_ad_row.metrics.cost_per_conversion,
                        "value_per_conversion": ad_group_ad_row.metrics.value_per_conversion,
                        "all_conversions_value": ad_group_ad_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": ad_group_ad_row.metrics.conversions_from_interactions_rate
                    }
                })

            def get_keyword(criterion_id):
                get_keyword_query = f"""
                    SELECT
                        ad_group_criterion.keyword.text,
                        ad_group_criterion.keyword.match_type
                    FROM
                        ad_group_criterion
                    WHERE
                        ad_group_criterion.criterion_id = {criterion_id}
                """ 
                keyword_response = ga_service.search(customer_id=id, query=get_keyword_query)
                for response in keyword_response:
                    keyword = response.ad_group_criterion.keyword
                    print(keyword)
                    return [keyword.text, keyword.match_type]
                
            for keyword_view_row in keyword_view_response:
                keyword_view_data.append({
                    "resource_name": keyword_view_row.keyword_view.resource_name,
                    "keyword_text": get_keyword(keyword_view_row.keyword_view.resource_name.split("~")[-1])[0],
                    "keyword_match_type": get_keyword(keyword_view_row.keyword_view.resource_name.split("~")[-1])[1],
                    "campaign_name": keyword_view_row.campaign.name,
                    "ad_group_name": keyword_view_row.ad_group.name,
                    "metrics": {
                        "cost_micros": keyword_view_row.metrics.cost_micros,
                        "conversions_value": keyword_view_row.metrics.conversions_value,
                        "clicks": keyword_view_row.metrics.clicks,
                        "interaction_rate": keyword_view_row.metrics.interaction_rate,
                        "view_through_conversions": keyword_view_row.metrics.view_through_conversions,
                        "average_cpc": keyword_view_row.metrics.average_cpc,
                        "conversions": keyword_view_row.metrics.conversions,
                        "ctr": keyword_view_row.metrics.ctr,
                        "all_conversions": keyword_view_row.metrics.all_conversions,
                        "cost_per_conversion": keyword_view_row.metrics.cost_per_conversion,
                        "value_per_conversion": keyword_view_row.metrics.value_per_conversion,
                        "all_conversions_value": keyword_view_row.metrics.all_conversions_value,
                        "conversions_from_interactions_rate": keyword_view_row.metrics.conversions_from_interactions_rate
                    }
                })

            results["keyword_views"] = keyword_view_data
            results["ad_group_ads"] = ad_group_ad_data
            results["ad_groups"] = ad_group_data
            results["campaigns"] = campaign_data
            marketing_data.append(results)

            return Response(marketing_data,status=status.HTTP_200_OK)
        except GoogleAdsException as ex:
            print(f"Request failed with status {ex.error.code().name} and includes the following errors:")
            for error in ex.failure.errors:
                print(f"\tError with message {error.message}.")
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")

            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#-----------------------------------------------------FACEBOOK--------------------------------------------------#

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
            email=email,
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

#-----------------------------------------------------TWITTER--------------------------------------------------#


# twitter - util functions

def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=twitter_client_id,
                                client_secret=twitter_client_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": verifier}
    access_token_data = oauth_token.post(url, data=data)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list

def twitter_get_oauth_request_token():
    global resource_owner_key
    global resource_owner_secret
    request_token = OAuth1Session(client_key=twitter_client_id, client_secret=twitter_client_secret, callback_uri=twitter_redirect_uri)
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    callback_confirmed = str.split(data_token[2], '=')[1] if len(data_token) > 2 else None
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    if callback_confirmed != 'true':
        return Response(
            {"detail": "Unauthorized request error!!!"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
    

@api_view(("GET",))
def twitter_oauth(request):
    try:
        twitter_get_oauth_request_token()
        url = "https://api.twitter.com/oauth/authenticate?oauth_token=" + resource_owner_key

        print(url)
     
        return Response({
            "url": url},
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
def twitter_oauth_callback(request):
    try:
        if not request.query_params.get("oauth_verifier"):
            return Response(
                {"detail": "something not working???"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        oauth_verifier  = request.query_params.get("oauth_verifier")
        oauth_list = twitter_get_oauth_token(oauth_verifier,resource_owner_key,resource_owner_secret)
        
        access_token = {}
        print(oauth_list)
        for token in oauth_list:
            key, value = token.split('=')
            access_token[key] = value

        key = access_token['oauth_token'] # life long validity until revoked
        secret = access_token['oauth_token_secret']
        
        # Create OAuth1Session with the obtained access token
        oauth_user = OAuth1Session(client_key=twitter_client_id,
                                client_secret=twitter_client_secret,
                                resource_owner_key=key,
                                resource_owner_secret=secret)
        
        url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        params = {"include_email": True}
        user_data = oauth_user.get(url_user, params=params)
        user_json = user_data.json()
        email = user_json.get('email', None)   # gets email only if twitter account connected with email else None

        print(email)
        print(resource_owner_key, resource_owner_secret, key, secret)

        twitter_channel = get_channel(
            email=email,
            channel_type_num=3
        )


        twitter_channel.credentials.key_1= resource_owner_key
        twitter_channel.credentials.key_2= resource_owner_secret
        twitter_channel.credentials.key_3 = key
        twitter_channel.credentials.key_4 = secret
        twitter_channel.credentials.key_5 = email
        twitter_channel.credentials.save()

        return redirect("http://localhost:3001/channels/")

    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def get_twitter_ad_accounts(auth):
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts'
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        accounts = data['data']
        account_list = []
        for i in accounts:
            account_list.append(i['id'])
        return account_list
    else:
        print(f'Failed to fetch ad accounts: {response.status_code}')
        print('Response:', response.text)
        return None
    
def get_twitter_campaign_data(auth, account_id):
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/campaigns'
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        campaign_data = data['data']
        campaign_data_list = []
        for single_campaign in campaign_data:
            campaign_data_dict = {
                "id" : single_campaign.get("id"),
                "name": single_campaign.get("name"),
                "entity_status": single_campaign.get("entity_status"),
                "created_at": single_campaign.get("created_at"),
                "duration_in_days": single_campaign.get("duration_in_days"),
                "total_budget_amount_local_micro": single_campaign.get("total_budget_amount_local_micro"),
                "daily_budget_amount_local_micro": single_campaign.get("daily_budget_amount_local_micro"),
            }
            campaign_data_list.append(campaign_data_dict)
        
        return campaign_data_list
    else:
        print(f'Failed to fetch ad accounts: {response.status_code}')
        print('Response:', response.text)
        return None

def get_twitter_line_items_data(auth, account_id):
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/line_items'
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        data = response.json()
        line_items_data_long = data['data']
        line_items_data_list = []
        for line_items_data in line_items_data_long:
            line_items_data_dict = {
                "id" : line_items_data.get("id"),
                "name": line_items_data.get("name"),
                "campaign_id": line_items_data.get("campaign_id"),
                "objective": line_items_data.get("objective"),
                "placements": line_items_data.get("placements"),
                "goal": line_items_data.get("goal"),
                "product_type": line_items_data.get("product_type"),
                "start_time": line_items_data.get("start_time"),
                "end_time": line_items_data.get("end_time"),
            }
            line_items_data_list.append(line_items_data_dict)
        
        return line_items_data_list
    else:
        print(f'Failed to fetch ad accounts: {response.status_code}')
        print('Response:', response.text)
        return None
    
def get_twitter_active_entities_data(auth, account_id):
    url = f'{twitter_ads_api_url}{twitter_api_version}/stats/accounts/{account_id}/active_entities'

    all_active_entities = []
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)
    start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    entities = ['CAMPAIGN', 'FUNDING_INSTRUMENT', 'LINE_ITEM', 'MEDIA_CREATIVE', 'PROMOTED_ACCOUNT', 'PROMOTED_TWEET']

    for entity in entities:
        params = {
            'start_time': start_time,
            'end_time': end_time,
            'entity': entity
        }

        response = requests.get(url, params=params, auth=auth)

        if response.status_code == 200:
            data = response.json()
            entity_data_long = data['data']
            entity_data_list = []
            for entity_data in entity_data_long:
                entity_data_dict = {
                    "entity_type": entity,
                    "entity_id": entity_data.get("entity_id"),
                    "activity_start_time": entity_data.get("activity_start_time"),
                    "activity_end_time": entity_data.get("activity_end_time"),
                    "placements": entity_data.get("placements")[0],
                }
                entity_data_list.append(entity_data_dict)
            all_active_entities.append({entity: entity_data_list})
        else:
            print(f'Failed to fetch active entities for {entity}: {response.status_code}')
            print('Response:', response.text)

    return all_active_entities if all_active_entities else None

def fetch_entity_stats(auth, account_id, entities_info):
    url = f'{twitter_ads_api_url}{twitter_api_version}/stats/accounts/{account_id}'
    granularity = 'TOTAL'
    metric_groups = 'ENGAGEMENT'
    results = []
    end_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)
    start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    for entity_info in entities_info:
        for entity_type, entities in entity_info.items():
            for entity in entities:
                params = {
                    'entity': entity_type,
                    'entity_ids': entity['entity_id'],
                    'start_time': str(start_time),
                    'end_time': str(end_time),
                    'granularity': granularity,
                    'placement': entity['placements'],
                    'metric_groups': metric_groups
                }

                response = requests.get(url, params=params, auth=auth)

                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        'entity_type': entity_type,
                        'entity_id': entity['entity_id'],
                        'statistics': data
                    })
                else:
                    print(f'Failed to fetch stats for {entity_type} {entity["entity_id"]}: {response.status_code}')
                    print('Response:', response.text)
    
    return results


def get_promoted_tweets(auth, account_id):
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/promoted_tweets'

    response = requests.get(url, auth=auth)
    response.raise_for_status()
    
    promoted_tweets = response.json()
    tweet_ids = [tweet['tweet_id'] for tweet in promoted_tweets['data']]
    
    return tweet_ids

def get_tweet_details(auth, account_id, tweet_ids):

    if(len(tweet_ids) == 0):
        return "NA"
    tweet_ids_str = ','.join(tweet_ids)
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/tweets?tweet_ids={tweet_ids_str}&tweet_type=PUBLISHED&trim_user=true'

    response = requests.get(url, auth=auth)
    response.raise_for_status()
    
    tweet_details = response.json()
    tweet_data = tweet_details['data']
    tweet_data_list = []
    for i in tweet_data:
        medias = []
        for j in i['entities']['media']:
            medias.append({
                "media_url": j['media_url'],
                "type": j['type']
            })
        hashtag_list = []
        for x in i['entities']['hashtags']:
            hashtag_list.append(x['text'])
        tweet_data_dict = {
            "media": medias,
            "hashtags": hashtag_list ,
            "retweet_count" : i['retweet_count'],
            "full_text" : i['full_text'],
            "favorite_count": i['favorite_count'],
            "tweet_type": i['tweet_type'],
            "lang": i['lang']
        }
    tweet_data_list.append(tweet_data_dict)
    return tweet_data_list

def get_media_creatives(auth, account_id):
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/media_creatives'

    response = requests.get(url, auth=auth)
    response.raise_for_status()
    
    media_creatives = response.json()
    account_media_ids = [media['account_media_id'] for media in media_creatives['data']]
    
    return account_media_ids

def get_media_details(auth, account_id, account_media_ids):
    if (len(account_media_ids) == 0):
        return "NA"
    account_media_ids_str = ','.join(account_media_ids)
    url = f'{twitter_ads_api_url}{twitter_api_version}/accounts/{account_id}/account_media?account_media_ids={account_media_ids_str}'

    response = requests.get(url, auth=auth)
    response.raise_for_status()
    
    media_details = response.json()
    return media_details['data']


@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def get_twitter_marketing_data(access_token, access_token_secret):
# def get_twitter_marketing_data(request):

    auth = OAuth1(os.getenv("TWITTER_CLIENT_ID"), os.getenv("TWITTER_CLIENT_SECRET"), access_token, access_token_secret)


    accounts = get_twitter_ad_accounts(auth)
    marketing_data = []
    try:    
        for account_id in accounts:
            campaigns_data = get_twitter_campaign_data(auth, account_id)

            line_items_data = get_twitter_line_items_data(auth, account_id)

            entities_info = get_twitter_active_entities_data(auth, account_id)
            
            entities_with_stats = fetch_entity_stats(auth, account_id, entities_info)

            tweet_ids = get_promoted_tweets(auth, account_id)
            
            tweet_details = get_tweet_details(auth,account_id, tweet_ids)
            
            account_media_ids = get_media_creatives(auth,account_id)
            
            media_details = get_media_details(auth, account_id, account_media_ids)
            
            marketing_data_dict = {
                "account_id": account_id,
                "campaigns_data": campaigns_data,
                "line_items_data": line_items_data,
                "entities_and_statistics": entities_with_stats,
                "tweets_data": tweet_details,
                "media_data": media_details
            }

            marketing_data.append(marketing_data_dict)
        
        return Response(
            marketing_data,
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("Error :", e)
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#-----------------------------------------------------LINKEDIN--------------------------------------------------#

@api_view(("GET",))
def linkedin_oauth(request):
    try:
        authorization_url, state = linkedin.authorization_url(url=linkedin_authorization_base_url, state=passthrough_val)
        print(authorization_url)
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
def linkedin_oauth_callback(request):
    try:
        if request.query_params.get("state") != passthrough_val:
            return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        redirect_response = request.build_absolute_uri()

        token = linkedin.fetch_token(token_url=linkedin_token_url, client_secret=linkedin_client_secret,  #60 days validity
                             include_client_id=True,
                             authorization_response=redirect_response)

        access_token = token.get("access_token") # 60 days
        refresh_token = token.get("refresh_token") # 365 days
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            }

        response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)

        user_details = response.json()

        email = user_details.get("email")

        print(access_token, refresh_token, email)

        linkedin_channel = get_channel(
            email=email,
            channel_type_num=4
        )

        linkedin_channel.credentials.key_1= access_token
        linkedin_channel.credentials.key_2= refresh_token
        linkedin_channel.credentials.save()

        return redirect("http://localhost:3001/channels/")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

def get_linkedin_ad_accounts(access_token):
    url = "https://api.linkedin.com/v2/adAccountsV2?q=search&search.type.values[0]=BUSINESS&search.status.values[0]=ACTIVE"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    account_list = []
    if response.status_code == 200:
        accounts = response.json().get("elements", [])
        for account in accounts:
            item = {
                "account_id": account['id'],
                "account_name": account['name']
            }
            account_list.append(item)
        return account_list
    else:
        print("Failed to fetch ad accounts", response.status_code, response.text)

def get_linkedin_campaigns(access_token, account_id):
    
    account_urn = f'urn:li:sponsoredAccount:{account_id}'
    url = f"https://api.linkedin.com/v2/adCampaignsV2?q=search&search.account.values[0]={account_urn}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    campaign_list = []
    if response.status_code == 200:
        campaigns = response.json().get("elements", [])
        for campaign in campaigns:
            item = {
                "id": campaign.get('id'),
                "name": campaign.get('name'),
                "status": campaign.get('status'),
                "created": campaign['changeAuditStamps']['created']['time'],
                "lastModified": campaign['changeAuditStamps']['lastModified']['time'],
                "costType": campaign.get('costType'),
                "totalBudget": campaign.get('totalBudget'),
                "unitCost": campaign.get('unitCost'),
                "type": campaign.get('type'),
                "locale": campaign.get('locale')
            }
            campaign_list.append(item)
        return campaign_list
    else:
        print("Failed to fetch campaigns", response.status_code, response.text)

def get_linkedin_ad_creatives(access_token, campaign_id):
    print(campaign_id)
    campaign_urn = f'urn:li:sponsoredCampaign:{campaign_id}'
    url = f"https://api.linkedin.com/v2/adCreativesV2?q=search&search.campaign.values[0]={campaign_urn}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        ad_creatives = response.json()
        creative = ad_creatives['elements'][0]
        ad_creatives_dict = {
                "id": creative.get('id'),
                "status": creative.get('status'),
                "type": creative.get('type'),
                "campaign": creative.get('campaign'),
                "created": creative['changeAuditStamps']['created']['time'],
                "lastModified": creative['changeAuditStamps']['lastModified']['time'],
                "variables": creative.get('variables'),
                "reference": creative.get('reference'),
                "reference_content": [],   
            }
        return ad_creatives_dict
    else:
        return {'error': response.json()}

def get_post_details(access_token, post_urn):
    encoded_urn = urllib.parse.quote(post_urn)
    url = f"https://api.linkedin.com/v2/posts/{encoded_urn}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        post_data = response.json()
        post_content = {
            "content": post_data.get("content"),
            "contentLandingPage": post_data.get("contentLandingPage"),
            "commentary": post_data.get("commentary")
        }
        return post_content
    
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }
    
# def get_linkedin_ad_analytics(access_token, sponsoredaccount_id):
#     url = (
#         f"https://api.linkedin.com/v2/adAnalytics?q=statistics&dateRange=(start:(day:1,month:1,year:2024),end:(day:30,month:5,year:2024))&timeGranularity=ALL&accounts=List(urn%3Ali%3AsponsoredAccount%3A{sponsoredaccount_id})&pivots=List(CREATIVE,CAMPAIGN)&fields=impressions,clicks,totalEngagements,comments,shares,reactions,approximateUniqueImpressions,externalWebsiteConversions,externalWebsitePostClickConversions,externalWebsitePostViewConversions,conversionValueInLocalCurrency,oneClickLeads,pivot,pivotValues,pivotValue&projection=(*,elements*(*,pivotValues(*~sponsoredCampaign(id,name,type,objectiveType,status,campaignGroup~(id,name,status))~sponsoredCreative(status,type))))"
#     )
    
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#         'LinkedIn-Version': '202401',
#         'X-Restli-Protocol-Version': '2.0.0'
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  
#         return response.json() 
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")
#     except Exception as err:
#         print(f"Other error occurred: {err}")

@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def get_linkedin_marketing_data(access_token):
    try:
        account_list = get_linkedin_ad_accounts(access_token)
        marketing_data = []
        for account in account_list:
            # marketing data dictionary (structure)
            account_data = {
            'account_id': "",
            'account_name':"",
            'campaign_data': {
                "details": [],
                "ad_creatives": {
                    "data": [],
                    "analytics": [],
                    "statistics": [],
                    "adbudgetstats":[]
                }
            },
            }

            # add account related data
            account_data['account_id'] = account.get("account_id")
            account_data['account_name'] = account.get("account_name")
            
            #add campaign related data
            account_data['campaign_data']['details'] = get_linkedin_campaigns(access_token, account.get("account_id"))
            ad_creative_list = []
            for campaign in account_data['campaign_data']['details']:
                ad_creative = get_linkedin_ad_creatives(access_token, campaign.get('id') )
                ad_creative['reference_content'] = get_post_details(access_token, ad_creative['reference'])
                ad_creative_list.append(ad_creative)

                # ad analytic endpoints are not configured (yet to be done)
                # get_linkedin_ad_analytics(access_token, account.get("account_id") )

            account_data['campaign_data']['data'] = ad_creative_list
            
            
            marketing_data.append(account_data)

        print(marketing_data)
        return Response(
        status=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"Exception found: {e}")
        return Response(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#-----------------------------------------------------TIKTOK--------------------------------------------------#

@api_view(("GET",))
def tiktok_oauth(request):
    try:
        csrf_state = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        url = "https://www.tiktok.com/v2/auth/authorize/"
        url += f"?client_key={os.getenv('TIKTOK_CLIENT_ID')}"
        url += "&scope=ads.read,ads.management,user.info"
        url += "&response_type=code"
        url += f"&redirect_uri={tiktok_redirect_uri}"
        url += "&state=" + csrf_state

        return Response({
            "url": url},
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
def tiktok_oauth_callback(request):
    try:
        if request.query_params.get("state") != passthrough_val:
            return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        redirect_response = request.build_absolute_uri()

        token = tiktok.fetch_token(token_url=tiktok_token_url, authorization_response=redirect_response, client_secret=tiktok_client_secret)

        print(token)

        # aryan
        # add token to tiktok model
        # no email here!
        tiktok_channel = get_channel(
            email= request.user.email,
            channel_type_num=5
        )

        tiktok_channel.credentials.key_1= token
        tiktok_channel.save()

        return redirect("http://localhost:3001/channels/")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_tiktok_marketing_data(access_token):
    #aryan
    # pass access token from tiktok model
    base_url = "https://ads.tiktok.com/open_api/2/"
    headers = {
        "access_token": access_token,
        "Content-Type": "application/json"
    }

    accounts_url = base_url + "advertiser/get/"
    accounts_response = requests.get(accounts_url, headers=headers)
    accounts_data = accounts_response.json()
    advertiser_ids = [account['advertiser_id'] for account in accounts_data['data']['list']]

    all_data = {}

    for advertiser_id in advertiser_ids:
        campaign_url = base_url + "campaign/get/"
        campaign_params = {
            "advertiser_id": advertiser_id
        }
        campaign_response = requests.get(campaign_url, headers=headers, params=campaign_params)
        campaign_data = campaign_response.json()

        adgroup_url = base_url + "adgroup/get/"
        adgroup_params = {
            "advertiser_id": advertiser_id
        }
        adgroup_response = requests.get(adgroup_url, headers=headers, params=adgroup_params)
        adgroup_data = adgroup_response.json()

        ad_url = base_url + "ad/get/"
        ad_params = {
            "advertiser_id": advertiser_id
        }
        ad_response = requests.get(ad_url, headers=headers, params=ad_params)
        ad_data = ad_response.json()

        performance_url = base_url + "reports/get/"
        performance_params = {
            "advertiser_id": advertiser_id,
            "start_date": "2022-01-01",
            "end_date": "2022-12-31",
            "time_granularity": "daily",
            "metrics": ["impressions", "clicks", "ctr", "video_views", "conversions", "conversion_rate", "cost_per_conversion", "likes", "shares", "comments", "engagement_rate", "spend", "cpm", "cpc", "roi"],
            "dimensions": ["ad_id", "date"]
        }
        performance_response = requests.get(performance_url, headers=headers, params=performance_params)
        performance_data = performance_response.json()

        all_data[advertiser_id] = {
            "campaign_data": campaign_data,
            "adgroup_data": adgroup_data,
            "ad_data": ad_data,
            "performance_data": performance_data
        }

    return all_data