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
from requests_oauthlib import OAuth1Session, OAuth1
from django.shortcuts import redirect
from datetime import datetime, timedelta
from oauth.external_urls import twitter_ads_api_url,twitter_authorization_base_url,twitter_redirect_uri,twitter_token_url,frontend_channel_url
from oauth.helper import get_channel,create_channel

load_dotenv(override=True)

#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

"""
APP - CONFIGURATIONS
"""
twitter_client_id = os.getenv("TWITTER_CLIENT_ID")
twitter_client_secret = os.getenv("TWITTER_CLIENT_SECRET")
twitter_scopes = ["email", "ads_read", "ads_management"]
twitter_api_version = '11'
resource_owner_key = ''
resource_owner_secret = ''



def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=twitter_client_id,
                                client_secret=twitter_client_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    data = {"oauth_verifier": verifier}
    access_token_data = oauth_token.post(twitter_token_url, data=data)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list


def twitter_get_oauth_request_token(subspace_id):
    global resource_owner_key
    global resource_owner_secret
    
    callback_with_state = f"{twitter_redirect_uri}?subspace_id={subspace_id}"
    request_token = OAuth1Session(client_key=twitter_client_id, client_secret=twitter_client_secret, callback_uri=callback_with_state)
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
    subspace_id = request.query_params.get("subspace_id")
    try:
        twitter_get_oauth_request_token(subspace_id)
        url = f"{twitter_authorization_base_url}?oauth_token={resource_owner_key}"
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
        subspace_id = request.query_params.get('subspace_id')
        print(subspace_id,"subspace_id")
        if not request.query_params.get("oauth_verifier"):
            return Response(
                {"detail": "OAuth verifier is missing"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        oauth_verifier = request.query_params.get("oauth_verifier")
        oauth_list = twitter_get_oauth_token(oauth_verifier, resource_owner_key, resource_owner_secret)
        
        access_token = {}
        for token in oauth_list:
            key, value = token.split('=')
            access_token[key] = value

        key = access_token['oauth_token']
        secret = access_token['oauth_token_secret']
        
        oauth_user = OAuth1Session(client_key=twitter_client_id,
                                   client_secret=twitter_client_secret,
                                   resource_owner_key=key,
                                   resource_owner_secret=secret)
        
        url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        params = {"include_email": True}
        user_data = oauth_user.get(url_user, params=params)
        user_json = user_data.json()
        twitter_email = user_json.get('email', None)  

        if not subspace_id:
            return Response(
                {"detail": "Unable to retrieve subspace of the user"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        
        try:
            twitter_channel = get_channel(subspace_id=subspace_id, channel_type_num=3)
        except Exception:
            twitter_channel = create_channel(subspace_id=subspace_id, channel_type_num=3)
            print(twitter_channel)

        if twitter_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=resource_owner_key,
                key_2=resource_owner_secret,
                key_3=key,
                key_4=secret,
                key_5=twitter_email
            )
            twitter_channel.credentials = credentials
        else:
            twitter_channel.credentials.key_1 = resource_owner_key
            twitter_channel.credentials.key_2 = resource_owner_secret
            twitter_channel.credentials.key_3 = key
            twitter_channel.credentials.key_4 = secret
            twitter_channel.credentials.key_5 = twitter_email
            twitter_channel.credentials.save()

        twitter_channel.save()
        return redirect(frontend_channel_url)

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



def get_twitter_marketing_data(access_token, access_token_secret):

    try:    
        auth = OAuth1(os.getenv("TWITTER_CLIENT_ID"), os.getenv("TWITTER_CLIENT_SECRET"), access_token, access_token_secret)

        accounts = get_twitter_ad_accounts(auth)
        marketing_data = {
            "channel": "Twitter/X Channel",
            "channel_data": []
        }
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

            marketing_data["channel_data"].append(marketing_data_dict)
        
        return marketing_data

    except Exception as e:
        print("Error in Fetching Twitter Channel Data:" + str(e))
        return None
