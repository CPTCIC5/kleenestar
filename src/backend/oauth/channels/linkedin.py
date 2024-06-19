from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from channels.models import APICredentials
import hashlib
import urllib.parse 
import os
import json
import base64
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from django.shortcuts import redirect
from oauth.helper import get_channel,create_channel
from oauth.external_urls import frontend_channel_url,linkedin_authorization_base_url,linkedin_redirect_uri,linkedin_token_url
load_dotenv(override=True)



#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()


"""
APP - CONFIGURATIONS
"""
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_scope = ["r_ads_reporting", "r_ads","rw_ads","r_organization_admin", "email","openid","profile","r_organization_social"]
linkedin = OAuth2Session(linkedin_client_id, redirect_uri=linkedin_redirect_uri, scope=linkedin_scope)


@api_view(("GET",))
def linkedin_oauth(request):
    state_dict = {'email': request.user.email, 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()

    try:
        authorization_url, state = linkedin.authorization_url(url=linkedin_authorization_base_url, state=state_encoded)
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
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        if state_params.get("passthrough_val", None) != passthrough_val:
            return Response(
            {"detail": "State token does not match the expected state."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        redirect_response = request.build_absolute_uri()

        user_email = state_params.get("email", None)
        if not user_email:
            return Response(
                {"detail": "Unable to retrieve user email"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

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
        try:
            linkedin_channel = get_channel(email=user_email, channel_type_num=4)
        except Exception:
            linkedin_channel = create_channel(email=user_email, channel_type_num=4)
        
        if linkedin_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token,
                key_2=refresh_token,
            )
            linkedin_channel.credentials = credentials
        else:
            linkedin_channel.credentials.key_1 = access_token
            linkedin_channel.credentials.key_2 = refresh_token
            linkedin_channel.credentials.save()

        linkedin_channel.save()

        return redirect(frontend_channel_url)


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
    campaign_urn = f'urn:li:sponsoredCampaign:{campaign_id}'
    url = f"https://api.linkedin.com/v2/adCreativesV2?q=search&search.campaign.values[0]={campaign_urn}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        ad_creatives = response.json()
        creatives = ad_creatives['elements']
        creatives_list = []
        for creative in creatives:
            creatives_list.append({
                    "id": creative.get('id'),
                    "status": creative.get('status'),
                    "type": creative.get('type'),
                    "campaign": creative.get('campaign'),
                    "created": creative['changeAuditStamps']['created']['time'],
                    "lastModified": creative['changeAuditStamps']['lastModified']['time'],
                    "variables": creative.get('variables'),
                    "reference": creative.get('reference'),
                    "reference_content": [],   
                })
        return creatives_list
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
    
def get_linkedin_ad_analytics(access_token, sponsoredcampaign_id):
    url = (
        f"https://api.linkedin.com/v2/adAnalyticsV2?q=statistics&dateRange.start.day=1&dateRange.start.month=1&dateRange.start.year=2024&dateRange.end.day=10&dateRange.end.month=6&dateRange.end.year=2024&timeGranularity=MONTHLY&campaigns=urn:li:sponsoredCampaign:{sponsoredcampaign_id}&pivots=CAMPAIGN&fields=impressions,clicks,comments,shares,reactions,costInLocalCurrency,externalWebsiteConversions,approximateUniqueImpressions"
    )
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '1.0.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.json().get("elements", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


def get_organization_urns(access_token):
    url = "https://api.linkedin.com/v2/organizationAcls?q=roleAssignee"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        organization_urns = [org['organization'] for org in data.get('elements', [])]
        return organization_urns
    else:
        print(f"Failed to retrieve organizations: {response.status_code}")
        return []

def get_posts_for_organization(access_token, organization_urn_list):
    post_details_list = []

    for element in organization_urn_list:

        url = f"https://api.linkedin.com/v2/posts?author={element}&q=author"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            post_data = data.get("elements", [])
            for post in post_data:

                insights_url = f"https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={element}&ugcPosts[0]={post['id']}"

                response = requests.get(insights_url, headers=headers)

                insights_data = response.json()


                post_details_list.append({
                    "id": post['id'],
                    "content": post["content"],
                    "commentary": post["commentary"],
                    "insights": insights_data.get("elements", [])
                })
    return post_details_list



def get_linkedin_marketing_data(access_token):
    try:
        marketing_data = [{"channel_type": "LinkedIn Channel"}]
        account_list = get_linkedin_ad_accounts(access_token)
        for account in account_list:
            # marketing data dictionary (structure)
            account_data = {
            'account_id': "",
            'account_name':"",
            'campaign_data': {
                "details": [],
                "ad_creatives": []
            },
            "post_data" : []

            }

            # add account related data
            account_data['account_id'] = account.get("account_id")
            account_data['account_name'] = account.get("account_name")
            
            # add campaign related data
            account_data['campaign_data']['details'] = get_linkedin_campaigns(access_token, account.get("account_id"))
            
            for campaign in account_data['campaign_data']['details']:
                ad_creatives = get_linkedin_ad_creatives(access_token, campaign.get('id') )
                ad_creative_list = []
                for ad_creative in ad_creatives:
                    ad_creative_dict = {}
                    ad_creative_dict['reference_content'] = get_post_details(access_token, ad_creative['reference'])
                    ad_creative_dict['data'].append(ad_creative)
                    ad_creative_dict['statistics'].append(get_linkedin_ad_analytics(access_token,  campaign.get('id') ))
                    ad_creative_list.append(ad_creative_dict)
                account_data["campaign_data"]["ad_creatives"] = ad_creative_list
            marketing_data.append(account_data)

        organization_list = get_organization_urns(access_token)
        post_details = get_posts_for_organization(access_token, organization_list)

        marketing_data.append({
            "post_data": post_details
        })

        return marketing_data
    
    except Exception as e:
        print("Error in Fetching Linkedin Channel Data:" + str(e))
        return None
