from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from app_channels.models import APICredentials
import hashlib
import urllib.parse 
import os
import json
import base64
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
from django.shortcuts import redirect
from oauth.helper import get_channel,create_channel
from oauth.external_urls import frontend_channel_url, bing_redirect_uri, bing_token_url, bing_scopes
load_dotenv(override=True)



#state value for oauth request authentication
passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()


"""
APP - CONFIGURATIONS
"""
bing_client_id = os.getenv('BING_CLIENT_ID')
bing_client_secret = os.getenv('BING_CLIENT_SECRET')




@api_view(("GET",))
def bing_oauth(request):    
    state_dict = {'subspace_id': request.query_params.get("subspace_id"), 'passthrough_val': passthrough_val}
    state_json = json.dumps(state_dict)
    state_encoded = base64.urlsafe_b64encode(state_json.encode()).decode()

    try:
        authorization_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={bing_client_id}&response_type=code&redirect_uri={bing_redirect_uri}&response_mode=query&scope={urllib.parse.quote(' '.join(bing_scopes))}&state={state_encoded}"
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
def bing_oauth_callback(request):
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
            'client_id': bing_client_id,
            'client_secret': bing_client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': bing_redirect_uri,
            'scope': 'https://ads.microsoft.com/msads.manage offline_access'
        }

        response = requests.post(bing_token_url, data=data)

        token = response.json()

        access_token = token.get("access_token") # 60 days
        refresh_token = token.get("refresh_token") # 365 days
        
        print(access_token, refresh_token)
        
        try:
            bing_channel = get_channel(subspace_id=subspace_id, channel_type_num=11)
        except Exception:
            bing_channel = create_channel(subspace_id=subspace_id, channel_type_num=11)
        
        if bing_channel.credentials is None:
            credentials = APICredentials.objects.create(
                key_1=access_token,
                key_2=refresh_token,
            )
            bing_channel.credentials = credentials
        else:
            bing_channel.credentials.key_1 = access_token
            bing_channel.credentials.key_2 = refresh_token
            bing_channel.credentials.save()

        bing_channel.save()

        return redirect(f"{frontend_channel_url}/{subspace_id}/")


    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return Response(
            {"detail": "An error occurred during the OAuth process"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

