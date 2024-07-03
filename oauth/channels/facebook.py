from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from channels.models import APICredentials
import hashlib
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from dotenv import load_dotenv
from django.shortcuts import redirect
import requests
from oauth.helper import create_channel, get_channel
from oauth.external_urls import facebook_api_url, facebook_authorization_base_url, facebook_redirect_uri, facebook_token_url, frontend_channel_url

import json
import base64

load_dotenv(override=True)

# state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

# APP - CONFIGURATIONS
# facebook
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")

facebook_scopes = ['ads_read', 'ads_management', 'public_profile', 'email', 'pages_show_list', 'pages_read_engagement', 'pages_read_user_content']
facebook = OAuth2Session(facebook_client_id, redirect_uri=facebook_redirect_uri, scope=facebook_scopes)
facebook = facebook_compliance_fix(facebook)

@api_view(("GET",))
def facebook_oauth(request):
    subspace_id = request.query_params.get("subspace_id")
    state_dict = {'subspace_id': subspace_id, 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()

    print(os.getenv("FACEBOOK_CONFIG_ID"))
    try:
        authorization_url, state = facebook.authorization_url(url=facebook_authorization_base_url, state=state_encoded)

        return Response({
            "url": authorization_url + f"&config_id={os.getenv('FACEBOOK_CONFIG_ID')}"},
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
    try:
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        if state_params.get("passthrough_val") != passthrough_val:
            return Response(
                {"detail": "State token does not match the expected state."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        subspace_id = state_params.get("subspace_id")
        if not subspace_id:
            return Response(
                {"detail": "Unable to retrieve subspace of the user"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        redirect_response = request.build_absolute_uri()
        token = facebook.fetch_token(token_url=facebook_token_url, client_secret=facebook_client_secret, # 60days validity
                                     authorization_response=redirect_response) # access_token

        access_token = token.get("access_token")
        facebook_data = get_facebook_data(access_token)

        try:
            facebook_channel = get_channel(subspace_id=subspace_id, channel_type_num=2)
        except Exception:
            facebook_channel = create_channel(subspace_id=subspace_id, channel_type_num=2)

        if facebook_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token,
                key_2=facebook_data['ad_account_ids']
            )
            facebook_channel.credentials = credentials
        else:
            facebook_channel.credentials.key_1 = access_token
            facebook_channel.credentials.key_2 = facebook_data['ad_account_ids']
            facebook_channel.credentials.save()

        facebook_channel.save()

        return redirect(frontend_channel_url)

    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



def get_facebook_data(access_token):
    user_url = '{facebook_api_url}/me'
    ads_accounts_url = '{facebook_api_url}/me/adaccounts'

    user_params = {
        'fields': 'email',
        'access_token': access_token
    }

    ads_params = {
        'access_token': access_token
    }
    email = ""
    ad_account_ids = []

    user_response = requests.get(user_url, params=user_params)
    if user_response.status_code == 200:
        user_data = user_response.json()
        email = user_data.get('email')
    else:
        print(f"Error fetching user email: {user_response.status_code}")
        print(user_response.text)

    ads_response = requests.get(ads_accounts_url, params=ads_params)
    if ads_response.status_code == 200:
        ads_data = ads_response.json()
        ad_accounts = ads_data.get('data', [])
        ad_account_ids = [account['id'] for account in ad_accounts]
    else:
        print(f"Error fetching ad account IDs: {ads_response.status_code}")
        print(ads_response.text)

    return {
        'email': email,
        'ad_account_ids': ad_account_ids
    }


def get_facebook_campaign_data(access_token, account_list):
    campaign_account_list = []
    for account in account_list:
        campaign_url = f"{facebook_api_url}/{account}/campaigns"
        campaign_params = {
            "access_token": access_token,
            "effective_status": '["ACTIVE"]',
            "fields": 'name,objective,status,effective_status,start_time,stop_time,daily_budget,lifetime_budget,adsets'
        }
        response = requests.get(campaign_url,params=campaign_params)
        response.raise_for_status()
        campaign_data = response.json()['data']
        for campaign in campaign_data:
            campaign['adsets'] = campaign['adsets']['data']
        campaign_account_list.append(campaign_data)
    return campaign_account_list

def get_facebook_campaign_statistics(access_token, campaign_data):
    for account_campaings in campaign_data:
        for campaigns in account_campaings:
            campaign_insights_params = {
                'access_token': access_token,
                'date_preset': 'last_7d',  # gets the insights for the last 7 days.
                'fields': 'campaign_id,campaign_name,spend,impressions,clicks,reach,frequency,unique_clicks,cpm,cpp,cost_per_conversion,conversions,website_ctr'
            }
            campaign_insights_url = f"{facebook_api_url}/{campaigns['id']}/insights"
            response = requests.get(campaign_insights_url, params=campaign_insights_params)

            campaigns['insights'] = response.json()['data']

    return campaign_data

def get_page_posts(access_token):
    
    pages_url = f'{facebook_api_url}/me/accounts'
    
    pages_params = {
        'access_token': access_token
    }
    pages_response = requests.get(pages_url, params=pages_params)
    pages_data = pages_response.json().get('data', [])

    result = []
    
    for page in pages_data:
        page_id = page['id']
        page_name = page['name']
        page_access_token = page['access_token']
        
        posts_url = f'{facebook_api_url}/{page_id}/posts'
        
        posts_params = {
            'fields': 'id,message,created_time,story,permalink_url,attachments{media_type,url,media,title},comments.summary(true),reactions.summary(true),shares',
            'access_token': page_access_token
        }
        
        posts_response = requests.get(posts_url, params=posts_params)
        posts_data = posts_response.json().get('data', [])
        
        for post in posts_data:
            post_details = {
                'page_id': page_id,
                'page_name': page_name,
                'post_id': post.get('id'),
                'message': post.get('message'),
                'created_time': post.get('created_time'),
                'story': post.get('story'),
                'permalink_url': post.get('permalink_url'),
                'attachments': post.get('attachments', {}).get('data', []),
                'comments_count': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                'reactions_count': post.get('reactions', {}).get('summary', {}).get('total_count', 0),
                'shares_count': post.get('shares', {}).get('count', 0)
            }
            result.append(post_details)
    return result

def get_ads_creative_data(access_token, campaign_data):

    for account_campaings in campaign_data:
        
        for campaings in account_campaings:
            adsets_list = campaings['adsets']
            ads_data = []
            for adsets in adsets_list:
                ad_set_url = f"{facebook_api_url}/{adsets['id']}/ads"
                
                ad_set_params = {
                    "access_token" : access_token,
                    "fields": 'name,status,effective_status,creative'
                }

                response = requests.get(ad_set_url, params=ad_set_params)

                ads_data = response.json()['data']

                for ads in ads_data:
                    creative_url = f"{facebook_api_url}/{ads['creative']['id']}"
                    creative_params = {
                        'access_token' : access_token,
                        'fields': 'body,title,image_url'
                    }   
                    response = requests.get(creative_url, params=creative_params)
                    
                    ads['creative'] = response.json()

                adsets['ads_data'] = ads_data
        
        campaings['adsets'] = adsets_list

    return campaign_data

def get_adset_data(access_token, campaing_data):
    for account_campaings in campaing_data:    
        for campaings in account_campaings:
            adsets_list = campaings['adsets']
            adsets_data = []
            for adsets in adsets_list:
                ad_set_url = f"{facebook_api_url}/{adsets['id']}"
                
                ad_set_params = {
                    "access_token" : access_token,
                    "fields": 'name,status,effective_status,billing_event,optimization_goal,targeting'
                }

                response = requests.get(ad_set_url, params=ad_set_params)
                ad_set_data = response.json()
                ad_set_data['id'] = adsets['id']
                adsets_data.append(ad_set_data)
        
            campaings['adsets'] = adsets_data

    return campaing_data


def get_facebook_marketing_data(access_token, ad_account_list):
    marketing_data = []
    
    try:    
        campaign_data = get_facebook_campaign_data(access_token, ad_account_list)
        campaing_data = get_adset_data(access_token, campaign_data)
        campaign_data = get_ads_creative_data(access_token,campaing_data)
        campaign_data = get_facebook_campaign_statistics(access_token, campaign_data)
        post_details_data = get_page_posts(access_token)

        marketing_data = [{"channel": "Meta Channel"},campaign_data, post_details_data]

        return Response(
            marketing_data, status=status.HTTP_200_OK
        )
    
    except Exception as e:
        print(f"Error with message {e}.")
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
