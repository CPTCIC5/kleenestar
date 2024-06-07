from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel, APICredentials
import hashlib
import urllib.parse 
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from django.shortcuts import redirect
from users.models import User
load_dotenv()


def get_channel(email,channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]
    return get_object_or_404(Channel, channel_type=channel_type_num, workspace=workspace)

def create_channel(email, channel_type_num):
    user = get_object_or_404(User,email=email)
    workspace = user.workspace_set.all()[0]
    try:
        new_channel = Channel.objects.create(
            channel_type=channel_type_num, 
            workspace=workspace,
        )
        return new_channel
    except Exception:
        return Channel.objects.get(channel_type=channel_type_num, workspace=workspace,)

#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()


"""
APP - CONFIGURATIONS
"""
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_scope = ["r_ads_reporting", "r_ads", "r_organization_admin", "email","openid","profile","r_organization_social"]
linkedin_authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
linkedin_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
linkedin_redirect_uri = 'http://127.0.0.1:8000/api/oauth/linkedin-callback/'
linkedin = OAuth2Session(linkedin_client_id, redirect_uri=linkedin_redirect_uri, scope=linkedin_scope)



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
        try:
            linkedin_channel = get_channel(email=request.user.email, channel_type_num=4)
        except Exception:
            linkedin_channel = create_channel(email=request.user.email, channel_type_num=4)
        
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
