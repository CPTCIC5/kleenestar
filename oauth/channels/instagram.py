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
from oauth.external_urls import facebook_api_url, facebook_authorization_base_url, instagram_redirect_uri, facebook_token_url, frontend_channel_url

import json
import base64

load_dotenv(override=True)

# state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

# APP - CONFIGURATIONS
# facebook
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")

instagram_scope = [
    'instagram_basic',
    'instagram_content_publish',
    'instagram_manage_comments',
    'instagram_manage_insights',
    'instagram_shopping_tag_products',
    'pages_show_list',
    'pages_read_engagement'
]
facebook = OAuth2Session(facebook_client_id, redirect_uri=instagram_redirect_uri, scope=instagram_scope)
facebook = facebook_compliance_fix(facebook)

@api_view(("GET",))
def instagram_oauth(request):
    user_email = request.user.email
    state_dict = {'email': user_email, 'passthrough_val': passthrough_val}
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
def instagram_oauth_callback(request):   
    try:
        state_encoded = request.query_params.get('state')
        state_json = base64.urlsafe_b64decode(state_encoded).decode()
        state_params = json.loads(state_json)

        # if state_params.get("passthrough_val") != passthrough_val:
        #     return Response(
        #         {"detail": "State token does not match the expected state."},
        #         status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #     )

        user_email = state_params.get("email")
        if not user_email:
            return Response(
                {"detail": "Unable to retrieve user email"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        redirect_response = request.build_absolute_uri()
        token = facebook.fetch_token(token_url=facebook_token_url, client_secret=facebook_client_secret, # 60days validity
                                     authorization_response=redirect_response) # access_token

        access_token = token.get("access_token")
        facebook_data = get_facebook_data(access_token)
        print(facebook_data)

        try:
            instagram_channel = get_channel(email=user_email, channel_type_num=10)
        except Exception:
            instagram_channel = create_channel(email=user_email, channel_type_num=10)

        if instagram_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token
            )
            instagram_channel.credentials = credentials
        else:
            instagram_channel.credentials.key_1 = access_token
            instagram_channel.credentials.save()

        instagram_channel.save()

        return redirect(frontend_channel_url)

    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



def get_facebook_data(access_token):
   # Use the user access token to get the user's Pages
        pages_url = f"https://graph.instagram.com/v20.0/me/accounts"
        pages_params = {
            'access_token': access_token,
        }

        pages_response = requests.get(pages_url, params=pages_params)
        pages_data = pages_response.json()

        if 'error' in pages_data:
            return Response(
                {"detail": f"Error fetching user's Pages: {pages_data.get('error').get('message', 'Unknown error')}"}, 
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Assuming the user has at least one Page, get the first one
        pages = pages_data.get('data', [])
        if not pages:
            return Response(
                {"detail": "No Pages found for the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the Page ID and Page Access Token
        page_id = pages[0].get('id')
        page_access_token = pages[0].get('access_token')

        # Get the Instagram Business Account linked to the Page
        ig_account_url = f"https://graph.instagram.com/v20.0/{page_id}"
        ig_account_params = {
            'fields': 'instagram_business_account',
            'access_token': page_access_token,
        }

        ig_account_response = requests.get(ig_account_url, params=ig_account_params)
        ig_account_data = ig_account_response.json()

        if 'error' in ig_account_data:
            return Response(
                {"detail": f"Error fetching Instagram Business Account: {ig_account_data.get('error').get('message', 'Unknown error')}"}, 
                status=status.HTTP_400_BAD_REQUEST,
            )

        instagram_business_account = ig_account_data.get('instagram_business_account')

        if not instagram_business_account:
            return Response(
                {"detail": "No Instagram Business Account found for the Page."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return {
            "user_access_token": access_token,
            "page_id": page_id,
            "page_access_token": page_access_token,
            "instagram_business_account": instagram_business_account
        }


