from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from channels.models import Channel
import hashlib
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
from users.models import User
import json
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
tiktok_client_id = os.getenv('TIKTOK_CLIENT_ID')
tiktok_client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
# configured in tiktok app (browser)
# tiktok_redirect_uri = 'https://a7b1-2401-4900-57e1-6bfc-4182-80ff-5d55-cbdf.ngrok-free.app/api/oauth/tiktok-callback/'
tiktok_token_url = 'https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/'
tiktok_api_url = "https://business-api.tiktok.com/open_api"
tiktok_sandbox_api_url = "https://sandbox-ads.tiktok.com/open_api"






@api_view(("GET",))
def tiktok_oauth(request):
    try:
        authorization_url = f"https://business-api.tiktok.com/portal/auth?app_id={tiktok_client_id}&state={passthrough_val}&redirect_uri=https%3A%2F%2F5842-2401-4900-57d2-3eb7-6416-dc3-8af0-6e4f.ngrok-free.app%2Fapi%2Foauth%2Ftiktok-callback%2F"

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
        code = request.query_params.get("auth_code")
        if  code == None:
            return Response(
            {"detail": "code not found, invalid request."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "app_id": tiktok_client_id,
            "auth_code":  code,
            "secret": tiktok_client_secret,
        }
        response = requests.post(tiktok_token_url, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            return Response(
                {"detail": "An error occurred during the OAuth process: " + response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        access_token = response.json()['data']['access_token']  # does not expire
        advertiser_ids = response.json()['data']['advertiser_ids']
        tiktok_channel = get_channel(  # stores the access token to model
            email= request.user.email,
            channel_type_num=5
        )

        tiktok_channel.credentials.key_1= access_token
        tiktok_channel.credentials.key_2 = advertiser_ids 
        tiktok_channel.credentials.save()
        return redirect("http://localhost:3001/channels/")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_tiktok_campaign_data(access_token, advertiser_ids):

    campaign_account_data = []
    for advertiser_Id in advertiser_ids:
        print(advertiser_Id)
        campaign_url = f"{tiktok_sandbox_api_url}/campaign/get/?advertiser_id={advertiser_Id}"
        headers = {
            'Access-Token': access_token
        }
        campaign_list = []
        response = requests.get(campaign_url, headers=headers)
        campaign_data = response.json()
        print(campaign_data)
    #     response.raise_for_status()
    #     for campaign in campaign_list:
    #         campaign_list.append({

    #         })
    # return campaign_account_data


@csrf_exempt
@api_view(("GET",))
@permission_classes([AllowAny]) 
# def get_tiktok_marketing_data(access_token, advertiser_ids):
def get_tiktok_marketing_data(access_token):
    try:
        # access_token = "a8017ab343d6b56eea3bd68ddfcad3bd3a483032"
        access_token = "3c174dc93fb84d1f1d9f8b288941c0c6e668cd8f"
        # advertiser_account_list = get_tiktok_advertiser_id(access_token)
        advertiser_ids = ['7365545989899354113']
        get_tiktok_campaign_data(access_token, advertiser_ids)

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(f"Error in api: {e}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)







