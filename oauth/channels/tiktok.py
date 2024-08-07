from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from channels.models import APICredentials
import hashlib
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
import json
from oauth.helper import create_channel, get_channel
from oauth.external_urls import frontend_channel_url, tiktok_api_url, tiktok_sandbox_api_url, tiktok_token_url, tiktok_redirect_uri
from urllib.parse import quote
import json
import base64

load_dotenv(override=True)

# state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

"""
APP - CONFIGURATIONS
"""
tiktok_client_id = os.getenv('TIKTOK_CLIENT_ID')
tiktok_client_secret = os.getenv('TIKTOK_CLIENT_SECRET')

@api_view(("GET",))
def tiktok_oauth(request):
    user_email = request.user.email
    state_dict = {'email': user_email, 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()

    try:
        authorization_url = f"https://business-api.tiktok.com/portal/auth?app_id={tiktok_client_id}&state={state_encoded}&redirect_uri={quote(tiktok_redirect_uri)}"

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
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        if state_params.get("passthrough_val") != passthrough_val:
            return Response(
                {"detail": "State token does not match the expected state."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user_email = state_params.get("email")
        if not user_email:
            return Response(
                {"detail": "Unable to retrieve user email"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        code = request.query_params.get("auth_code")
        if code is None:
            return Response(
                {"detail": "code not found, invalid request."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "app_id": tiktok_client_id,
            "auth_code": code,
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

        try:
            tiktok_channel = get_channel(email=user_email, channel_type_num=5)
        except Exception:
            tiktok_channel = create_channel(email=user_email, channel_type_num=5)

        if tiktok_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token,
                key_2=advertiser_ids,
            )
            tiktok_channel.credentials = credentials
        else:
            tiktok_channel.credentials.key_1 = access_token
            tiktok_channel.credentials.key_2 = advertiser_ids
            tiktok_channel.credentials.save()

        tiktok_channel.save()
        return redirect(frontend_channel_url)

    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def get_tiktok_campaign_data(access_token, advertiser_ids):
    campaign_account_data = []
    for advertiser_id in advertiser_ids:
        campaign_url = f"{tiktok_sandbox_api_url}/campaign/get/?advertiser_id={advertiser_id}"
        headers = {
            'Access-Token': access_token
        }
        response = requests.get(campaign_url, headers=headers)
        campaign_data = response.json()
        if campaign_data['code'] == 0:
            campaign_account_data.extend(campaign_data['data']['list'])
    return campaign_account_data

def get_tiktok_adgroup_data(access_token, advertiser_ids):
    adgroup_account_data = []
    for advertiser_id in advertiser_ids:
        adgroup_url = f"{tiktok_sandbox_api_url}/adgroup/get/?advertiser_id={advertiser_id}"
        headers = {
            'Access-Token': access_token
        }
        response = requests.get(adgroup_url, headers=headers)
        adgroup_data = response.json()
        if adgroup_data['code'] == 0:
            adgroup_account_data.extend(adgroup_data['data']['list'])
    return adgroup_account_data

def get_tiktok_ad_data(access_token, advertiser_ids):
    ad_account_data = []
    for advertiser_id in advertiser_ids:
        ad_url = f"{tiktok_sandbox_api_url}/ad/get/?advertiser_id={advertiser_id}"
        headers = {
            'Access-Token': access_token
        }
        response = requests.get(ad_url, headers=headers)
        ad_data = response.json()
        if ad_data['code'] == 0:
            ad_account_data.extend(ad_data['data']['list'])
    return ad_account_data

def get_tiktok_creative_metrics(access_token, advertiser_ids, material_type):
    creative_metrics_data = []
    for advertiser_id in advertiser_ids:
        metrics_url = f"{tiktok_sandbox_api_url}/creative/report/get/?advertiser_id={advertiser_id}&material_type={material_type}&metrics_fields=[\"spend\",\"impressions\",\"reach\",\"cpc\",\"cpm\",\"clicks\",\"ctr\",\"cost_per_conversion\",\"conversion_rate\"]"
        headers = {
            'Access-Token': access_token
        }
        response = requests.get(metrics_url, headers=headers)
        metrics_data = response.json()
        if metrics_data['code'] == 0:
            creative_metrics_data.extend(metrics_data['data']['list'])
    return creative_metrics_data

def get_tiktok_ultimate_report(access_token, advertiser_ids):
    ultimate_report_data = []
    for advertiser_id in advertiser_ids:
        report_url = f"{tiktok_sandbox_api_url}/report/integrated/get/"
        headers = {
            'Access-Token': access_token
        }
        
        payload = {
            "advertiser_id": advertiser_id,
            "service_type": "AUCTION",
            "report_type": "BASIC",
            "data_level": "AUCTION_AD",
            "dimensions": ["campaign_id"],
            "metrics": ["spend", "impressions", "reach", "cpc", "cpm", "clicks", "ctr", "cost_per_conversion", "conversion_rate", "likes", "comments", "shares", "follows"],
            "filtering": [{"field_name": "ad_status", "filter_type": "IN", "filter_value": "[\"STATUS_ALL\"]"}],
            "query_lifetime": True,
            "page": 1,
            "page_size": 200
        }
        response = requests.get(report_url, headers=headers, params=payload)
        report_data = response.json()
        if report_data['code'] == 0:
            ultimate_report_data.extend(report_data['data']['list'])
    return ultimate_report_data


def get_tiktok_marketing_data(access_token, advertiser_ids):
    try:
        campaign_data = get_tiktok_campaign_data(access_token, advertiser_ids)
        adgroup_data = get_tiktok_adgroup_data(access_token, advertiser_ids)
        ad_data = get_tiktok_ad_data(access_token, advertiser_ids)
        video_metrics = get_tiktok_creative_metrics(access_token, advertiser_ids, "VIDEO")
        image_metrics = get_tiktok_creative_metrics(access_token, advertiser_ids, "IMAGE")
        instant_page_metrics = get_tiktok_creative_metrics(access_token, advertiser_ids, "INSTANT_PAGE")
        ultimate_report = get_tiktok_ultimate_report(access_token, advertiser_ids)

        marketing_data = {
            "channel_type" : "Tiktok Channel",
            "campaign_data": campaign_data,
            "adgroup_data": adgroup_data,
            "ad_data": ad_data,
            "video_metrics": video_metrics,
            "image_metrics": image_metrics,
            "instant_page_metrics": instant_page_metrics,
            "ultimate_report": ultimate_report
        }

        return Response(marketing_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(f"Error in API: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)





