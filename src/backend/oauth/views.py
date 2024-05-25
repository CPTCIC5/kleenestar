from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel
import hashlib
import os
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
from requests_oauthlib import OAuth1Session
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
resource_owner_key = ''
resource_owner_secret = ''

#linkedin
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_scope = ["r_ads_reporting", "r_ads", "r_organization_admin", "email","openid","profile"]
linkedin_authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
linkedin_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
linkedin_redirect_uri = 'http://127.0.0.1:8000/api/oauth/linkedin-callback/'
linkedin = OAuth2Session(linkedin_client_id, redirect_uri=linkedin_redirect_uri, scope=linkedin_scope)

#tiktok
tiktok_client_id = os.getenv('TIKTOK_CLIENT_ID')
tiktok_client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
tiktok_redirect_uri = 'http://127.0.0.1:8000/api/oauth/tiktok-callback/'
tiktok_authorization_base_url = 'https://business-api.tiktok.com/open_api/v1.2/oauth/authorize/'
tiktok_token_url = 'https://business-api.tiktok.com/open_api/v1.2/oauth/token/'
tiktok_scopes = ['ads.read', 'ads.management','user.info']
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

        if isinstance(resource_names, list):
            return Response(
                {"detail": "manager accounts not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        customer_id = resource_names[0].split('/')[1]
        
        print(customer_id)
        
        google_channel = get_channel(
            email=email,
            channel_type_num=1
        )
        
        print(google_channel.credentials, "creds")
        print(google_channel,"channels")
        google_channel.credentials.key_1 = refresh_token
        print(google_channel.credentials.key_1, "key")
        google_channel.credentials.key_2 = access_token
        google_channel.credentials.key_3 = customer_id
        google_channel.credentials.save()
        
        
        return redirect("http://localhost:3001/channels/")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_google_marketing_data(customer_id):
    # credentials = {'email': 'griffin@kleenestar.io', 'code': '4/0AdLIrYfexY4rjSmgtHYgetnURuaiR3g-l15a5p9FAshczs4juOH9KQW4uhBfAEk2vYy9bg', 'refresh_token': '1//0g85xxVT1qZOlCgYIARAAGBASNwF-L9IrH0qqgrCQHHV0rStYEb_r4YcyAw6LDyOKsfIZ3MhwZSnORgoKg2AoOqEOqTiowLUmRvA', 'access_token': 'ya29.a0AXooCgvwSOWcRwHL3pweYXOkph__srmWKy7a5RuQXg1mOXqpVDFUsIQCIhZ4FWjRrp3CwFgUM_lJ-VqzEGI89rkqJUUbmvLRPhD8njsiyPsMVAeDEbl_C8VXyzgy_E7smRWN4s65MjTbuG3Ov3rJchJW81DwmiLWHdcoaCgYKAdISARISFQHGX2MiPs0SUQOlHKqRl1oS1zENpw0171', 'customer_id': '1766667019'}

    customer_id = "1766667019"
    credentials["refresh_token"] = "1//0g85xxVT1qZOlCgYIARAAGBASNwF-L9IrH0qqgrCQHHV0rStYEb_r4YcyAw6LDyOKsfIZ3MhwZSnORgoKg2AoOqEOqTiowLUmRvA"
    
        
    google_client = GoogleAdsClient.load_from_dict(credentials , version='v16')
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.serving_status,
            campaign.advertising_channel_type,
            campaign.start_date,
            campaign.end_date,
            campaign_budget.amount_micros,
            campaign.target.cpa_micros,
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group_ad.ad.id,
            ad_group_ad.ad.name,
            ad_group_ad.status,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.type,
            ad_group_ad.ad.text_ad.description,
            keyword_view.resource_name,
            keyword_plan_campaign_keyword.text,
            keyword_plan_campaign_keyword.match_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.average_cpc,
            metrics.ctr,
            metrics.conversions,
            metrics.conversion_rate,
            metrics.cost_per_conversion,
            metrics.all_conversions,
            metrics.click_conversion_rate,
            metrics.value_per_conversion,
            metrics.all_conversion_value,
            segments.age_range,
            segments.gender,
            segments.device,
            segments.location,
            segments.date,
            metrics.conversions_value,
            metrics.all_conversions_value,
            metrics.view_through_conversions,
            metrics.interaction_rate,
            metrics.average_position,
            segments.week,
            segments.month,
            segments.quarter,
            segments.year
        FROM
            campaign
        WHERE
            campaign.status = 'ENABLED'
    """

    ga_service = google_client.get_service("GoogleAdsService")
    
    try:
        response = ga_service.search(customer_id=customer_id, query=query)

        results = []
        for row in response:
            result = {
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "campaign_status": row.campaign.status,
                "campaign_serving_status": row.campaign.serving_status,
                "campaign_advertising_channel_type": row.campaign.advertising_channel_type,
                "campaign_start_date": row.campaign.start_date,
                "campaign_end_date": row.campaign.end_date,
                "campaign_budget": row.campaign_budget.amount_micros,
                "campaign_target_cpa": row.campaign.target.cpa_micros,
                "ad_group_id": row.ad_group.id,
                "ad_group_name": row.ad_group.name,
                "ad_group_status": row.ad_group.status,
                "ad_id": row.ad_group_ad.ad.id,
                "ad_name": row.ad_group_ad.ad.name,
                "ad_status": row.ad_group_ad.status,
                "ad_final_urls": row.ad_group_ad.ad.final_urls,
                "ad_type": row.ad_group_ad.ad.type,
                "ad_description": row.ad_group_ad.ad.text_ad.description,
                "keyword_resource_name": row.keyword_view.resource_name,
                "keyword_text": row.keyword_plan_campaign_keyword.text,
                "keyword_match_type": row.keyword_plan_campaign_keyword.match_type,
                "metrics_impressions": row.metrics.impressions,
                "metrics_clicks": row.metrics.clicks,
                "metrics_cost_micros": row.metrics.cost_micros,
                "metrics_average_cpc": row.metrics.average_cpc,
                "metrics_ctr": row.metrics.ctr,
                "metrics_conversions": row.metrics.conversions,
                "metrics_conversion_rate": row.metrics.conversion_rate,
                "metrics_cost_per_conversion": row.metrics.cost_per_conversion,
                "metrics_all_conversions": row.metrics.all_conversions,
                "metrics_click_conversion_rate": row.metrics.click_conversion_rate,
                "metrics_value_per_conversion": row.metrics.value_per_conversion,
                "metrics_all_conversion_value": row.metrics.all_conversion_value,
                "segments_age_range": row.segments.age_range,
                "segments_gender": row.segments.gender,
                "segments_device": row.segments.device,
                "segments_location": row.segments.location,
                "segments_date": row.segments.date,
                "metrics_conversions_value": row.metrics.conversions_value,
                "metrics_all_conversions_value": row.metrics.all_conversions_value,
                "metrics_view_through_conversions": row.metrics.view_through_conversions,
                "metrics_interaction_rate": row.metrics.interaction_rate,
                "metrics_average_position": row.metrics.average_position,
                "segments_week": row.segments.week,
                "segments_month": row.segments.month,
                "segments_quarter": row.segments.quarter,
                "segments_year": row.segments.year
            }
            results.append(result)

        print(results)

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
        print(token)
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
        facebook_channel.save()

        return redirect("http://localhost:3001/channels/")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

def get_facebook_marketing_data(access_token,ad_account_id):
    #aryan 
    # pass access_token and iterate by passing all the account id from db.

    FacebookAdsApi.init(access_token=access_token)
    ad_account = AdAccount(ad_account_id)

    fields = [
        'campaign_id', 'campaign_name', 'objective', 'campaign_status', 'campaign_effective_status',
        'campaign_start_time', 'campaign_stop_time', 'campaign_daily_budget', 'campaign_lifetime_budget',
        'adset_id', 'adset_name', 'adset_status', 'adset_effective_status', 'billing_event', 'optimization_goal',
        'targeting', 'ad_id', 'ad_name', 'ad_status', 'ad_effective_status', 'creative_body', 'creative_title',
        'creative_image_url', 'impressions', 'reach', 'frequency', 'unique_clicks', 'cpm', 'cpp', 'conversions',
        'cost_per_conversion', 'conversion_rate', 'website_ctr', 'clicks', 'cost_per_click', 'social_clicks',
        'social_impressions', 'spend', 'roi', 'purchase_roas', 'value_per_conversion', 'date_start', 'date_stop'
    ]

    params = {
        'level': 'ad',
        'time_range': {'since': '2023-01-01', 'until': '2023-12-31'},
        'filtering': [],
        'breakdowns': [],
    }

    insights = ad_account.get_insights(fields=fields, params=params)

    results = []
    for insight in insights:
        result = {
            "campaign_id": insight.get('campaign_id'),
            "name": insight.get('campaign_name'),
            "objective": insight.get('objective'),
            "status": insight.get('campaign_status'),
            "effective_status": insight.get('campaign_effective_status'),
            "start_time": insight.get('campaign_start_time'),
            "stop_time": insight.get('campaign_stop_time'),
            "daily_budget": insight.get('campaign_daily_budget'),
            "lifetime_budget": insight.get('campaign_lifetime_budget'),
            "adset_id": insight.get('adset_id'),
            "adset_name": insight.get('adset_name'),
            "adset_status": insight.get('adset_status'),
            "adset_effective_status": insight.get('adset_effective_status'),
            "billing_event": insight.get('billing_event'),
            "optimization_goal": insight.get('optimization_goal'),
            "targeting": {
                "age_min": insight.get('targeting', {}).get('age_min'),
                "age_max": insight.get('targeting', {}).get('age_max'),
                "genders": insight.get('targeting', {}).get('genders'),
                "geo_locations": insight.get('targeting', {}).get('geo_locations'),
                "interests": insight.get('targeting', {}).get('interests')
            },
            "ad_id": insight.get('ad_id'),
            "ad_name": insight.get('ad_name'),
            "ad_status": insight.get('ad_status'),
            "ad_effective_status": insight.get('ad_effective_status'),
            "creative": {
                "body": insight.get('creative_body'),
                "title": insight.get('creative_title'),
                "image_url": insight.get('creative_image_url')
            },
            "impressions": insight.get('impressions'),
            "reach": insight.get('reach'),
            "frequency": insight.get('frequency'),
            "unique_clicks": insight.get('unique_clicks'),
            "cpm": insight.get('cpm'),
            "cpp": insight.get('cpp'),
            "conversions": insight.get('conversions'),
            "cost_per_conversion": insight.get('cost_per_conversion'),
            "conversion_rate": insight.get('conversion_rate'),
            "website_ctr": insight.get('website_ctr'),
            "clicks": insight.get('clicks'),
            "cost_per_click": insight.get('cost_per_click'),
            "social_clicks": insight.get('social_clicks'),
            "social_impressions": insight.get('social_impressions'),
            "spend": insight.get('spend'),
            "roi": insight.get('roi'),
            "purchase_roas": insight.get('purchase_roas'),
            "value_per_conversion": insight.get('value_per_conversion'),
            "date_start": insight.get('date_start'),
            "date_stop": insight.get('date_stop')
        }
        results.append(result)

    print(results)


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

        # twitter_channel = get_channel(
        #     email=email,
        #     channel_type_num=3
        # )


        # twitter_channel.credentials.key_1= resource_owner_key
        # twitter_channel.credentials.key_2= resource_owner_secret
        # twitter_channel.credentials.key_3 = key
        # twitter_channel.credentials.key_4 = secret
        # twitter_channel.credentials.key_5 = email
        # twitter_channel.save()

        return redirect("http://localhost:3001/channels/")

    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_twitter_marketing_data(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    # aryan
    # get these credentials from twitter db and pass it to the function

    twitter_client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    accounts = twitter_client.accounts()
    for account in accounts:
        data = {
            "campaigns": [],
            "line_items": [],
            "ads": [],
            "audience_metrics": [],
            "conversion_metrics": [],
            "engagement_metrics": [],
            "revenue_metrics": [],
            "time_metrics": []
        }

        # Fetch campaigns
        for campaign in Campaign.all(account):
            data["campaigns"].append({
                "id": campaign.id,
                "name": campaign.name,
                "entity_status": campaign.entity_status,
                "start_time": campaign.start_time,
                "end_time": campaign.end_time,
                "daily_budget_amount_local_micro": campaign.daily_budget_amount_local_micro,
                "total_budget_amount_local_micro": campaign.total_budget_amount_local_micro
            })

        # Fetch line items
        for line_item in LineItem.all(account):
            data["line_items"].append({
                "id": line_item.id,
                "name": line_item.name,
                "campaign_id": line_item.campaign_id,
                "objective": line_item.objective,
                "placements": line_item.placements
            })

        # Fetch ads (Promoted Tweets)
        for ad in PromotedTweet.all(account):
            data["ads"].append({
                "id": ad.id,
                "tweet_id": ad.tweet_id,
                "line_item_id": ad.line_item_id,
                "entity_status": ad.entity_status,
                "approval_status": ad.approval_status,
                "created_at": ad.created_at,
                "updated_at": ad.updated_at
            })

        # Fetch analytics (audience, conversion, engagement, revenue, and time-based metrics)
        analytics = Analytics.all(
            account,
            entity='CAMPAIGN',
            metric_groups=[
                'ENGAGEMENT', 'VIDEO', 'WEB_CONVERSION', 'MOBILE_CONVERSION',
                'BILLING', 'MEDIA', 'LIFE_TIME_VALUE_MOBILE_CONVERSION'
            ],
            granularity='TOTAL'
        )

        for stat in analytics:
            data["audience_metrics"].append({
                "impressions": stat['impressions'],
                "reach": stat.get('reach'),  # Reach might not be directly available
                "engagements": stat['engagements'],
                "engagement_rate": stat['engagement_rate']
            })
            data["conversion_metrics"].append(stat['activity_metrics'])
            data["engagement_metrics"].append({
                "follows": stat['follows'],
                "likes": stat['likes'],
                "replies": stat['replies'],
                "retweets": stat['retweets']
            })
            data["revenue_metrics"].append({
                "billed_charge_local_micro": stat['billed_charge_local_micro'],
                "cpm": stat['cpm'],
                "cpc": stat['cpc']
            })
            data["time_metrics"].append({
                "start_time": stat['start_time'],
                "end_time": stat['end_time']
            })

        print(data)

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

        # linkedin_channel = get_channel(
        #     email=email,
        #     channel_type_num=4
        # )

        # linkedin_channel.credentials.key_1= access_token
        # linkedin_channel.credentials.key_2= refresh_token
        # linkedin_channel.credentials.key_3 = email
        # linkedin_channel.save()

        return redirect("http://localhost:3001/channels/")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

# @csrf_exempt
@api_view(("GET",))
# @permission_classes([AllowAny]) 
def get_linkedin_marketing_data(access_token):
    # aryan
    # get the access_token from the model 
    # access_token = ??
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    base_url = "https://api.linkedin.com/v2"

    # Get Campaign Information
    try:
        campaigns_url = f"{base_url}/adCampaignsV2"
        response = requests.get(campaigns_url, headers=headers)
        campaigns = response.json().get('elements', [])
        print(response.json())
        campaign_data = []
        for campaign in campaigns:
            campaign_info = {
                'id': campaign.get('id'),
                'name': campaign.get('name'),
                'status': campaign.get('status'),
                'created': campaign.get('created'),
                'lastModified': campaign.get('lastModified'),
                'dailyBudget': campaign.get('dailyBudget'),
                'totalBudget': campaign.get('totalBudget'),
                'objective': campaign.get('objective'),
                'type': campaign.get('type'),
            }
            
            # Get Ad Set
            ad_creatives_url = f"{base_url}/adCreativesV2?q=campaign&campaign={campaign['id']}"
            ad_response = requests.get(ad_creatives_url, headers=headers)
            ad_creatives = ad_response.json().get('elements', [])

            ad_creative_data = []
            for ad in ad_creatives:
                ad_info = {
                    'id': ad.get('id'),
                    'campaignId': ad.get('campaign'),
                    'format': ad.get('format'),
                    'status': ad.get('status'),
                    'created': ad.get('created'),
                    'lastModified': ad.get('lastModified'),
                    'textAdTitle': ad.get('textAdTitle'),
                    'textAdDescription': ad.get('textAdDescription'),
                    'landingPageUrl': ad.get('landingPageUrl'),
                }
                ad_creative_data.append(ad_info)
            
            campaign_info['ad_creatives'] = ad_creative_data

            # Get Audience Metrics, Conversion Metrics, Revenue Metrics, and Time-based Metrics
            metrics_url = f"{base_url}/adAnalyticsV2?q=analytics&pivot=AD&timeGranularity=ALL&campaigns={campaign['id']}"
            metrics_response = requests.get(metrics_url, headers=headers)
            metrics = metrics_response.json().get('elements', [])

            audience_metrics = {
                'impressions': 0,
                'clicks': 0,
                'uniqueImpressions': 0,
                'uniqueClicks': 0,
                'totalEngagements': 0,
            }

            conversion_metrics = {
                'likes': 0,
                'shares': 0,
                'comments': 0,
                'socialActions': 0,
                'engagementRate': 0.0,
            }

            revenue_metrics = {
                'costInUsd': 0.0,
                'cpm': 0.0,
                'cpc': 0.0,
                'totalSpent': 0.0,
            }

            time_based_metrics = {
                'startDate': None,
                'endDate': None,
            }

            for metric in metrics:
                audience_metrics.update({
                    'impressions': metric.get('impressions', 0),
                    'clicks': metric.get('clicks', 0),
                    'uniqueImpressions': metric.get('uniqueImpressions', 0),
                    'uniqueClicks': metric.get('uniqueClicks', 0),
                    'totalEngagements': metric.get('totalEngagements', 0),
                })
                conversion_metrics.update({
                    'likes': metric.get('likes', 0),
                    'shares': metric.get('shares', 0),
                    'comments': metric.get('comments', 0),
                    'socialActions': metric.get('socialActions', 0),
                    'engagementRate': metric.get('engagementRate', 0.0),
                })
                revenue_metrics.update({
                    'costInUsd': metric.get('costInUsd', 0.0),
                    'cpm': metric.get('cpm', 0.0),
                    'cpc': metric.get('cpc', 0.0),
                    'totalSpent': metric.get('totalSpent', 0.0),
                })
                time_based_metrics.update({
                    'startDate': metric.get('startDate'),
                    'endDate': metric.get('endDate'),
                })
            
            campaign_info['audience_metrics'] = audience_metrics
            campaign_info['conversion_metrics'] = conversion_metrics
            campaign_info['revenue_metrics'] = revenue_metrics
            campaign_info['time_based_metrics'] = time_based_metrics

            campaign_data.append(campaign_info)
        print(campaign_data)

    except Exception as e:
        print(f"Exception found: {e}")
        return Response(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

#-----------------------------------------------------TIKTOK--------------------------------------------------#

@api_view(("GET",))
def tiktok_oauth(request):
    try:
        authorization_url, state = tiktok.authorization_url(url=tiktok_authorization_base_url, state=passthrough_val)
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
        # Fetch campaign information
        campaign_url = base_url + "campaign/get/"
        campaign_params = {
            "advertiser_id": advertiser_id
        }
        campaign_response = requests.get(campaign_url, headers=headers, params=campaign_params)
        campaign_data = campaign_response.json()

        # Fetch ad group information
        adgroup_url = base_url + "adgroup/get/"
        adgroup_params = {
            "advertiser_id": advertiser_id
        }
        adgroup_response = requests.get(adgroup_url, headers=headers, params=adgroup_params)
        adgroup_data = adgroup_response.json()

        # Fetch ad information
        ad_url = base_url + "ad/get/"
        ad_params = {
            "advertiser_id": advertiser_id
        }
        ad_response = requests.get(ad_url, headers=headers, params=ad_params)
        ad_data = ad_response.json()

        # Fetch ad performance data
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

        # Store all data in the dictionary
        all_data[advertiser_id] = {
            "campaign_data": campaign_data,
            "adgroup_data": adgroup_data,
            "ad_data": ad_data,
            "performance_data": performance_data
        }

    return all_data