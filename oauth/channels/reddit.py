from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from app_channels.models import APICredentials
import hashlib
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
from datetime import datetime, timedelta, timezone
import json
import base64
from oauth.helper import get_channel, create_channel
from oauth.external_urls import reddit_token_url, reddit_api_url, reddit_redirect_uri, frontend_channel_url
import requests.auth

load_dotenv(override=True)

# State value for OAuth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

reddit_client_id = os.getenv("REDDIT_CLIENT_ID_TEST")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET_TEST")
user_agent = "Kleenestar/1.0 by Powerful-Parsley4755"

@api_view(("GET",))
def reddit_oauth(request):
    state_dict = {'subspace_id': request.query_params.get("subspace_id"), 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()

    try:  
        authorization_url = (
            f'https://www.reddit.com/api/v1/authorize?client_id={reddit_client_id}'
            f'&response_type=code&state={state_encoded}&redirect_uri={reddit_redirect_uri}'
            f'&duration=permanent&scope=identity read account history mysubreddits adsread'
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

def reddit_refresh_token_exchange(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    auth = requests.auth.HTTPBasicAuth(reddit_client_id, reddit_client_secret)
    headers = {'User-Agent': user_agent}
    response = requests.post(reddit_token_url, auth=auth, data=data, headers=headers)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        
        return access_token
    else:
        return f"Error: {response.content}", response.status_code

@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
def reddit_oauth_callback(request):
    try:
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        if state_params.get("passthrough_val", None) != passthrough_val:
            return Response(
                {"detail": "State token does not match the expected state."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        subspace_id = state_params.get("subspace_id", None)
        if not subspace_id:
            return Response(
                {"detail": "Unable to retrieve subspace of the user"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        code = request.query_params.get('code')
        if not code:
            return Response(
                {"detail": "Code is missing in the redirect URI, invalid request!"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': reddit_redirect_uri
        }

        auth = requests.auth.HTTPBasicAuth(reddit_client_id, reddit_client_secret)
        headers = {'User-Agent': user_agent}
        response = requests.post(reddit_token_url, auth=auth, data=data, headers=headers)

        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']

            print(access_token, refresh_token)
            
            try:
                reddit_channel = get_channel(subspace_id=subspace_id, channel_type_num=6)
            except Exception:
                reddit_channel = create_channel(subspace_id=subspace_id, channel_type_num=6)
            
            if reddit_channel.credentials is None:
                credentials = APICredentials.objects.create(
                    key_1=access_token,
                    key_2=refresh_token,
                )
                reddit_channel.credentials = credentials
            else:
                reddit_channel.credentials.key_1 = access_token
                reddit_channel.credentials.key_2 = refresh_token
                reddit_channel.credentials.save()

            reddit_channel.save()
            return redirect(f"{frontend_channel_url}/{subspace_id}/")
        
        else:
            return Response(
                {"detail": f"Error: {response.content}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def get_reddit_business_details(access_token):

    business_url = f"{reddit_api_url}/me/businesses"

    headers = {
        'Authorization': f'bearer {access_token}'
         ,'User-Agent': user_agent
    }

    response = requests.get(business_url, headers=headers)
    response.raise_for_status()
    business_details = response.json()['data'][0]
    business_dict = {
        "id": business_details.get("id"),
        "name": business_details.get("name"),
        "industry": business_details.get("industry")
    }
    return business_dict
    

def get_reddit_ad_accounts(access_token, business_id):

    accounts_url = f"{reddit_api_url}/businesses/{business_id}/ad_accounts"
    headers = {
        'Authorization': f'bearer {access_token}'
         ,'User-Agent': user_agent
    }
    response = requests.get(accounts_url, headers=headers)
    response.raise_for_status()
    accounts_data = response.json()['data']
    account_list = []
    for account in accounts_data:
        account_list.append({
            "id": account.get("id"),
            "created_at": account.get("created_at"),
            "timezone": account.get("time_zone_id"),
            "name": account.get("name")
        })
    return account_list


def get_reddit_ads(access_token, account_list):
    ads_list_accounts = []
    for account in account_list:
        ads_url = f"{reddit_api_url}/ad_accounts/{account.get('id')}/ads"
        headers = {
            'Authorization': f'bearer {access_token}'
             ,'User-Agent': user_agent
        }
        response = requests.get(ads_url, headers=headers)
        response.raise_for_status()
        ads_data = response.json()['data']

        ads_list = []
        for ads in ads_data:
            ads_list.append({
                "id": ads.get("id"),
                "name": ads.get("name"),
                "post_id": ads.get("post_id"),
                "post_url": ads.get("post_url"),
                "click_url": ads.get("click_url"),
                "ad_group_id": ads.get("ad_group_id"),
                "configured_status": ads.get("configured_status"),
                "created_at": ads.get("created_at")
            })
        ads_list_accounts.append(ads_list)
    return ads_list_accounts


def get_reddit_ad_group(access_token, ads_list_account):
    ad_group_list_accounts = []
    for ads_account in ads_list_account:
        ad_group_list = []
        for ads in ads_account:
            ad_group_url = f"{reddit_api_url}/ad_groups/{ads.get('ad_group_id')}"
            headers = {
                'Authorization': f'bearer {access_token}'
                 ,'User-Agent': user_agent
            }
            response = requests.get(ad_group_url, headers=headers)
            response.raise_for_status()
            ad_group = response.json()['data']
            ad_group_list.append({
                'adaccountandcampaigndetails': {
                    'adaccountid': ad_group.get('ad_account_id'),
                    'campaignid': ad_group.get('campaign_id'),
                    'adgroupid': ad_group.get('id'),
                    'name': ad_group.get('name')
                },
                'bidandbudgetinformation': {
                    'bidstrategy': ad_group.get('bid_strategy'),
                    'bidtype': ad_group.get('bid_type'),
                    'goaltype': ad_group.get('goal_type'),
                    'goalvalue': ad_group.get('goal_value')
                },
                'statusandscheduling': {
                    'configuredstatus': ad_group.get('configured_status'),
                    'effectivestatus': ad_group.get('effective_status'),
                    'starttime': ad_group.get('start_time'),
                    'endtime': ad_group.get('end_time')
                },
                'targetinginformation': {
                    'communities': ad_group.get('targeting', {}).get('communities'),
                    'geolocations': ad_group.get('targeting', {}).get('geolocations'),
                    'locations': ad_group.get('targeting', {}).get('locations'),
                    'expandtargeting': ad_group.get('targeting', {}).get('expand_targeting')
                },
                'optimizationandconversiongoals': {
                    'optimizationgoal': ad_group.get('optimization_goal'),
                    'viewthroughconversiontype': ad_group.get('view_through_conversion_type')
                },
                'timestamps': {
                    'createdat': ad_group.get('created_at'),
                    'modifiedat': ad_group.get('modified_at')
                }
            }
            )
        ad_group_list_accounts.append(ad_group_list)
    return ad_group_list_accounts


def get_reddit_campaign(access_token, ad_group_account_list):
    campaign_list_accounts = []
    for ads_account in ad_group_account_list:
        campaign_list = []
        for ads in ads_account:
            campaign_url = f"{reddit_api_url}/campaigns/{ads['adaccountandcampaigndetails']['campaignid']}"
            headers = {
                'Authorization': f'bearer {access_token}'
                 ,'User-Agent': user_agent
            }
            response = requests.get(campaign_url, headers=headers)
            response.raise_for_status()
            campaign = response.json()['data']
            campaign_list.append({
                "campaign_id": campaign.get("id"),
                "ad_account_id":campaign.get("ad_account_id"),
                "campaign_name":campaign.get("name"),
                "objective": campaign.get("objective"),
                "effective_status":campaign.get("effective_status"),
                "spend_cap": campaign.get("spend_cap"),
            })
        campaign_list_accounts.append(campaign_list)
    return campaign_list_accounts


def get_reddit_post(access_token, ads_list_accounts):
    post_list_accounts = []
    for ads_account in ads_list_accounts:
        post_list = []
        for ads in ads_account:
            post_url = f"{reddit_api_url}/posts/{ads['post_id']}"
            headers = {
                'Authorization': f'bearer {access_token}'
                 ,'User-Agent': user_agent
            }
            response = requests.get(post_url, headers=headers)
            response.raise_for_status()
            post = response.json()['data']
            post_list.append({
                "post_id": post.get("id"),
                "post_type":post.get("post_type"),
                "headline":post.get("headline"),
                "content": post.get("content"),
                "post_url":post.get("post_url"),
                "body": post.get("body"),
                "created_at": post.get("created_at")
            })
        post_list_accounts.append(post_list)
    return post_list_accounts


def get_reddit_report(access_token, account_list, start_date, end_date):
    campaign_insight_account_list = []
    for account in account_list:
        report_url = f"{reddit_api_url}/ad_accounts/{account['id']}/reports"
        headers = {
            'Authorization': f'bearer {access_token}'
             ,'User-Agent': user_agent,
            'Content-Type': 'application/json'  
        }
        config = {
            "data": {
                    "breakdowns": [
                    "CAMPAIGN_ID","AD_GROUP_ID", "AD_ID"
                ],
                "fields": [
                    "cpc", "spend", "region", "impressions", "interest", "keyword",
                    "key_conversion_clicks", "key_conversion_ecpa", "key_conversion_rate",
                    "key_conversion_total_count", "key_conversion_views", "cpv", "ctr",
                    "currency", "custom_event_name", "date", "dma", "ecpm",
                    "conversion_search_clicks", "clicks"
                ],
                "filter": "campaign:effective_status==ACTIVE",
                "starts_at": start_date,
                "ends_at": end_date
                }
        }
        response = requests.post(report_url, data=json.dumps(config), headers=headers)
        response.raise_for_status()
        report = response.json()['data']
        campaign_insight_account_list.append(report)
    return campaign_insight_account_list



def get_reddit_marketing_data(access_token):

    try:
        business_details = get_reddit_business_details(access_token)
        
        account_list = get_reddit_ad_accounts(access_token,business_details['id'])
        ads_list = get_reddit_ads(access_token, account_list)
        ad_group_list = get_reddit_ad_group(access_token, ads_list)
        campaign_list = get_reddit_campaign(access_token, ad_group_list)
        post_list = get_reddit_post(access_token, ads_list)
        # Retrive metrics for only 7 days
        start_date = (datetime.now(timezone.utc) - timedelta(days=7)).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:00:00Z')
        end_date = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:00:00Z')

        campaign_report_list = get_reddit_report(access_token, account_list, start_date, end_date)
        marketing_data_list = []
        
        for item in range(len(account_list)):
            marketing_data_dict = {}
            marketing_data_dict["account_data"] = account_list[item]
            marketing_data_dict["ad_group_data"] = ad_group_list[item]
            marketing_data_dict["ads_data"] = ads_list[item]
            marketing_data_dict["campaign_data"] = campaign_list[item]
            marketing_data_dict["post_data"] = post_list[item]
            marketing_data_dict["metrics_data"] = campaign_report_list[item]
            marketing_data_list.append(marketing_data_dict)


        reddit_marketing_data = {
            "channel": "Reddit",
            "business_details": business_details,
            "marketing_detials": marketing_data_list
        }

        return reddit_marketing_data
    
    except Exception as e:
        print("Error in Fetching Reddit Channel Data:" + str(e))
        return None